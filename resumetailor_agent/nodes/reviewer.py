from __future__ import annotations

from resumetailor_agent.config import AppConfig
from resumetailor_agent.llm import review_resume_output_with_llm


RISKY_PHRASES = (
    "independently",
    "expert",
    "large-scale",
    "architecture",
    "深度掌握",
    "精通",
    "主导",
)


RISK_ORDER = {"low": 0, "medium": 1, "high": 2}


def _pick_higher_risk(left: str, right: str) -> str:
    return left if RISK_ORDER.get(left, 0) >= RISK_ORDER.get(right, 0) else right


def _normalize_model_review(model_review: dict[str, object] | None) -> dict[str, object]:
    if not model_review:
        return {
            "enabled": False,
            "risk_level": "low",
            "issues": [],
            "evidence_gaps": [],
            "mode": "rule_only",
        }
    normalized = dict(model_review)
    normalized.setdefault("enabled", True)
    normalized.setdefault("risk_level", "low")
    normalized.setdefault("issues", [])
    normalized.setdefault("evidence_gaps", [])
    normalized.setdefault("mode", "llm_review")
    return normalized


def review_resume_output(
    resume_output: dict[str, object],
    evidence_texts: list[str],
    mode: str = "rule",
    config: AppConfig | None = None,
    model_review: dict[str, object] | None = None,
) -> dict[str, object]:
    evidence_blob = " ".join(evidence_texts).lower()
    issues: list[str] = []

    for section_value in resume_output.values():
        texts = section_value if isinstance(section_value, list) else [section_value]
        for text in texts:
            if not isinstance(text, str):
                continue
            lowered = text.lower()
            for phrase in RISKY_PHRASES:
                if phrase.lower() in lowered and phrase.lower() not in evidence_blob:
                    issues.append(f"Potentially unbacked claim: {text}")
                    break

    risk_level = "low"
    if issues:
        risk_level = "medium" if len(issues) == 1 else "high"
    if model_review is None:
        if config is not None:
            model_review = review_resume_output_with_llm(config, resume_output, evidence_texts)
        else:
            model_review = _normalize_model_review(None)
    normalized_model_review = _normalize_model_review(model_review)
    review_layers = ["rule"]
    merged_issues = list(issues)

    if normalized_model_review.get("enabled"):
        review_layers.append("model")
        for item in normalized_model_review.get("issues", []):
            if isinstance(item, str) and item not in merged_issues:
                merged_issues.append(item)
        risk_level = _pick_higher_risk(risk_level, str(normalized_model_review.get("risk_level", "low")))

    return {
        "risk_level": risk_level,
        "issues": merged_issues,
        "mode": mode,
        "review_layers": review_layers,
        "model_review": normalized_model_review,
    }
