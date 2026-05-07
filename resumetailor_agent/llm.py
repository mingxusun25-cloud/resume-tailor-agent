from __future__ import annotations

import json
from urllib import error, request

from resumetailor_agent.config import AppConfig
from resumetailor_agent.nodes.query_planner import tokenize


def _build_resume_prompt(
    jd_summary: dict[str, object], resume_output: dict[str, object], evidence_lines: list[str]
) -> str:
    return (
        "You are improving a resume tailoring draft.\n"
        "Keep all claims grounded in the provided evidence.\n"
        "Return JSON with keys: fit_summary, project_highlights, skills_summary, self_intro.\n\n"
        f"JD Summary: {json.dumps(jd_summary, ensure_ascii=False)}\n"
        f"Evidence: {json.dumps(evidence_lines, ensure_ascii=False)}\n"
        f"Draft: {json.dumps(resume_output, ensure_ascii=False)}\n"
    )


def _build_review_prompt(resume_output: dict[str, object], evidence_texts: list[str]) -> str:
    return (
        "You are reviewing a resume tailoring draft for unsupported claims.\n"
        "Only use the provided evidence. Return JSON with keys: risk_level, issues, evidence_gaps.\n\n"
        f"Evidence: {json.dumps(evidence_texts, ensure_ascii=False)}\n"
        f"Draft: {json.dumps(resume_output, ensure_ascii=False)}\n"
    )


def _chat_completion(config: AppConfig, prompt: str) -> dict[str, object]:
    payload = {
        "model": config.openai_model,
        "messages": [
            {"role": "system", "content": "You improve structured resume outputs."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "response_format": {"type": "json_object"},
    }
    req = request.Request(
        url=f"{config.openai_base_url.rstrip('/')}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.openai_api_key}",
        },
        method="POST",
    )
    with request.urlopen(req, timeout=config.llm_timeout_seconds) as response:
        body = json.loads(response.read().decode("utf-8"))
    content = body["choices"][0]["message"]["content"]
    return json.loads(content)


def _clean_string(value: object) -> str | None:
    if not isinstance(value, str):
        return None
    cleaned = value.strip()
    return cleaned or None


def _clean_string_list(value: object) -> list[str] | None:
    if not isinstance(value, list):
        return None
    cleaned = [item.strip() for item in value if isinstance(item, str) and item.strip()]
    return cleaned or None


MEANINGFUL_TOKEN_DENYLIST = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "that",
    "this",
    "have",
    "used",
    "using",
    "built",
    "candidate",
    "python",
    "agent",
    "workflow",
    "候选人",
    "具备",
    "相关",
    "实践",
    "经验",
    "项目",
    "能力",
}


def _meaningful_tokens(text: str) -> set[str]:
    return {
        token
        for token in tokenize(text)
        if len(token) > 1 and token not in MEANINGFUL_TOKEN_DENYLIST
    }


def _is_evidence_grounded(text: str, evidence_lines: list[str] | None) -> bool:
    if not evidence_lines:
        return True
    candidate_tokens = _meaningful_tokens(text)
    if not candidate_tokens:
        return True
    evidence_tokens = _meaningful_tokens(" ".join(evidence_lines))
    return bool(candidate_tokens & evidence_tokens)


def _merge_constrained_resume_output(
    resume_output: dict[str, object],
    enhanced: dict[str, object],
    evidence_lines: list[str] | None = None,
) -> dict[str, object]:
    merged = dict(resume_output)

    fit_summary = _clean_string(enhanced.get("fit_summary"))
    if fit_summary and _is_evidence_grounded(fit_summary, evidence_lines):
        merged["fit_summary"] = fit_summary

    project_highlights = _clean_string_list(enhanced.get("project_highlights"))
    if project_highlights:
        grounded_highlights = [
            item for item in project_highlights if _is_evidence_grounded(item, evidence_lines)
        ]
        if grounded_highlights:
            merged["project_highlights"] = grounded_highlights

    skills_summary = _clean_string(enhanced.get("skills_summary"))
    if skills_summary and _is_evidence_grounded(skills_summary, evidence_lines):
        merged["skills_summary"] = skills_summary

    self_intro = _clean_string(enhanced.get("self_intro"))
    if self_intro and _is_evidence_grounded(self_intro, evidence_lines):
        merged["self_intro"] = self_intro

    return merged


def review_resume_output_with_llm(
    config: AppConfig,
    resume_output: dict[str, object],
    evidence_texts: list[str],
) -> dict[str, object]:
    if not config.llm_enabled:
        return {
            "enabled": False,
            "risk_level": "low",
            "issues": [],
            "evidence_gaps": [],
            "mode": "rule_only",
        }

    try:
        response = _chat_completion(config, _build_review_prompt(resume_output, evidence_texts))
        risk_level = _clean_string(response.get("risk_level")) or "low"
        issues = _clean_string_list(response.get("issues")) or []
        evidence_gaps = _clean_string_list(response.get("evidence_gaps")) or []
        return {
            "enabled": True,
            "risk_level": risk_level,
            "issues": issues,
            "evidence_gaps": evidence_gaps,
            "mode": "llm_review",
        }
    except (error.URLError, TimeoutError, KeyError, json.JSONDecodeError, ValueError):
        return {
            "enabled": False,
            "risk_level": "low",
            "issues": [],
            "evidence_gaps": [],
            "mode": "fallback_rule_only",
        }


def enhance_resume_output(
    config: AppConfig,
    resume_output: dict[str, object],
    jd_summary: dict[str, object],
    evidence_lines: list[str],
) -> dict[str, object]:
    if not config.llm_enabled:
        result = dict(resume_output)
        result["llm_enhanced"] = False
        result["constraint_mode"] = "rule_only"
        return result

    try:
        enhanced = _chat_completion(config, _build_resume_prompt(jd_summary, resume_output, evidence_lines))
        merged = _merge_constrained_resume_output(
            resume_output,
            enhanced,
            evidence_lines=evidence_lines,
        )
        merged["llm_enhanced"] = True
        merged["constraint_mode"] = "llm_constrained"
        return merged
    except (error.URLError, TimeoutError, KeyError, json.JSONDecodeError, ValueError):
        fallback = dict(resume_output)
        fallback["llm_enhanced"] = False
        fallback["llm_error"] = "fallback_to_rule_mode"
        fallback["constraint_mode"] = "rule_only"
        return fallback
