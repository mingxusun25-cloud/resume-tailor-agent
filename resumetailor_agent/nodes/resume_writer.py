from __future__ import annotations

from collections import OrderedDict

from resumetailor_agent.schemas import EvidenceItem, JobRequirement


def build_resume_output(
    requirement: JobRequirement, evidence_items: list[EvidenceItem]
) -> dict[str, object]:
    grouped_details: OrderedDict[str, list[str]] = OrderedDict()
    matched_requirements_seen: set[str] = set()
    matched_requirements: list[str] = []

    for item in evidence_items:
        if item.chunk is None:
            continue
        summary = item.chunk.raw_text.strip().replace("\n", " ")
        grouped_details.setdefault(item.chunk.title, [])
        if summary not in grouped_details[item.chunk.title]:
            grouped_details[item.chunk.title].append(summary)
        if item.reason not in matched_requirements_seen:
            matched_requirements.append(item.reason)
            matched_requirements_seen.add(item.reason)

    project_highlights = [
        f"{title}: {' '.join(details)}" for title, details in grouped_details.items()
    ]

    skills_summary = ", ".join(requirement.keywords) if requirement.keywords else "No clear keywords extracted"
    fit_summary = (
        f"重点围绕 {skills_summary} 组织简历内容"
        if requirement.keywords
        else "需要补充更明确的岗位关键词"
    )
    self_intro = (
        f"候选人具备 {skills_summary} 相关实践，并能基于真实项目证据对齐该岗位需求。"
        if requirement.keywords
        else "候选人需要补充更明确的岗位关键词和项目证据。"
    )

    return {
        "fit_summary": fit_summary,
        "project_highlights": project_highlights,
        "skills_summary": skills_summary,
        "self_intro": self_intro,
        "matched_requirements": matched_requirements,
    }
