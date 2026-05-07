from __future__ import annotations

import re

from resumetailor_agent.schemas import JobRequirement, QueryPlan


SYNONYM_MAP: dict[str, tuple[str, ...]] = {
    "自动化": ("自动化", "automation", "workflow", "工作流"),
    "Agent": ("agent", "智能体"),
    "Python": ("python",),
    "RAG": ("rag", "retrieval", "retrieval-augmented"),
    "LLM": ("llm", "大模型"),
    "Streamlit": ("streamlit",),
}


TOKEN_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9+#\-.]*|[\u4e00-\u9fff]{2,}")


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


def _dedupe_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    for item in items:
        normalized = item.lower().strip()
        if not normalized or normalized in seen:
            continue
        seen.add(normalized)
        ordered.append(normalized)
    return ordered


def build_query_plan(requirement: JobRequirement) -> QueryPlan:
    query_parts = requirement.keywords + requirement.must_have + requirement.nice_to_have
    query_tokens: list[str] = []
    expanded_terms: list[str] = []

    for keyword in requirement.keywords:
        expanded_terms.extend(SYNONYM_MAP.get(keyword, (keyword.lower(),)))

    for part in query_parts:
        query_tokens.extend(tokenize(part))

    deduped_tokens = _dedupe_preserve_order(query_tokens)
    deduped_expanded_terms = _dedupe_preserve_order(expanded_terms + deduped_tokens)

    return QueryPlan(
        keywords=requirement.keywords[:],
        query_tokens=deduped_tokens,
        expanded_terms=deduped_expanded_terms,
        query_text=" ".join(deduped_expanded_terms),
    )
