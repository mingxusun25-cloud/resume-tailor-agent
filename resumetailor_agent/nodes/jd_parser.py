from __future__ import annotations

import re

from resumetailor_agent.schemas import JobRequirement


KEYWORD_PATTERNS: dict[str, tuple[str, ...]] = {
    "Python": ("python",),
    "RAG": ("rag",),
    "Agent": ("agent", "智能体"),
    "自动化": ("自动化", "automation", "workflow", "工作流"),
    "LLM": ("llm", "大模型"),
    "Streamlit": ("streamlit",),
}


def parse_job_description(jd_text: str) -> JobRequirement:
    lowered = jd_text.lower()
    keywords: list[str] = []

    for canonical, variants in KEYWORD_PATTERNS.items():
        if any(variant.lower() in lowered for variant in variants):
            keywords.append(canonical)

    must_have: list[str] = []
    nice_to_have: list[str] = []
    for fragment in re.split(r"[，。；;\n]", jd_text):
        cleaned = fragment.strip()
        if not cleaned:
            continue
        if any(marker in cleaned for marker in ("加分", "优先", "bonus", "plus")):
            nice_to_have.append(cleaned)
            continue
        if any(marker in cleaned for marker in ("要求", "熟悉", "经验", "掌握", "能力")):
            must_have.append(cleaned)

    job_title = ""
    first_segment = re.split(r"[，。\n]", jd_text)[0].strip()
    if first_segment:
        job_title = first_segment

    target_level = ""
    if "实习" in jd_text:
        target_level = "intern"
    elif "校招" in jd_text or "应届" in jd_text:
        target_level = "new_grad"

    return JobRequirement(
        job_title=job_title,
        keywords=keywords,
        must_have=must_have,
        nice_to_have=nice_to_have,
        target_level=target_level,
        resume_focus=keywords[:],
    )
