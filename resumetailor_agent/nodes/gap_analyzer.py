from __future__ import annotations

from resumetailor_agent.nodes.retriever import SYNONYM_MAP
from resumetailor_agent.schemas import EvidenceItem, JobRequirement


SUGGESTION_LIBRARY: dict[str, dict[str, str]] = {
    "RAG": {
        "action": "补一段检索增强或知识库问答经历",
        "evidence_hint": "写清召回、排序、输出链路",
    },
    "LLM": {
        "action": "补一段大模型应用或提示词约束实践",
        "evidence_hint": "写清输入约束、输出结构和失败回退",
    },
    "Streamlit": {
        "action": "补一段界面展示或调试面板实现",
        "evidence_hint": "写清输入区、结果区和中间结果可视化",
    },
    "Agent": {
        "action": "补一段工作流编排或多节点协作经历",
        "evidence_hint": "写清节点职责、上下文传递和失败处理",
    },
}


def build_gap_output(
    requirement: JobRequirement, evidence_items: list[EvidenceItem]
) -> dict[str, object]:
    searchable_parts: list[str] = []
    for item in evidence_items:
        if item.chunk is None:
            continue
        searchable_parts.append(item.chunk.title)
        searchable_parts.append(item.chunk.raw_text)

    evidence_blob = " ".join(searchable_parts).lower()
    matched_keywords: list[str] = []
    missing_keywords: list[str] = []

    for keyword in requirement.keywords:
        variants = SYNONYM_MAP.get(keyword, (keyword.lower(),))
        if any(variant.lower() in evidence_blob for variant in variants):
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    weak_requirements: list[str] = []
    for item in requirement.must_have:
        lowered = item.lower()
        if not lowered or lowered in evidence_blob:
            continue
        if any(keyword.lower() in lowered for keyword in matched_keywords):
            continue
        weak_requirements.append(item)

    if not requirement.keywords or not missing_keywords:
        gap_level = "low"
    elif len(missing_keywords) == len(requirement.keywords):
        gap_level = "high"
    else:
        gap_level = "medium"

    suggestion_cards: list[dict[str, str]] = []
    suggestions: list[str] = []
    for keyword in missing_keywords:
        template = SUGGESTION_LIBRARY.get(
            keyword,
            {
                "action": f"补充可证明 {keyword} 的项目细节或实验结果",
                "evidence_hint": "优先写清动作、工具和结果",
            },
        )
        card = {
            "keyword": keyword,
            "action": template["action"],
            "evidence_hint": template["evidence_hint"],
        }
        suggestion_cards.append(card)
        suggestions.append(f"{card['keyword']}: {card['action']}；{card['evidence_hint']}")

    return {
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
        "weak_requirements": weak_requirements,
        "gap_level": gap_level,
        "suggestions": suggestions,
        "suggestion_cards": suggestion_cards,
    }
