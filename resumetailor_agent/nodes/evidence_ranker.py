from __future__ import annotations

from resumetailor_agent.schemas import EvidenceItem, JobRequirement


def rank_evidence_items(
    requirement: JobRequirement, evidence_items: list[EvidenceItem], top_k: int = 5
) -> list[EvidenceItem]:
    del requirement
    sorted_items = sorted(evidence_items, key=lambda current: current.score, reverse=True)
    ranked: list[EvidenceItem] = []
    used_chunk_ids: set[str] = set()
    seen_titles: set[str] = set()

    for item in sorted_items:
        title = item.chunk.title if item.chunk else item.chunk_id
        if title in seen_titles:
            continue
        ranked.append(item.model_copy(update={"score": item.score + 0.4}))
        used_chunk_ids.add(item.chunk_id)
        seen_titles.add(title)
        if len(ranked) >= top_k:
            ranked.sort(key=lambda current: current.score, reverse=True)
            return ranked

    title_counts: dict[str, int] = {}
    for item in ranked:
        title = item.chunk.title if item.chunk else item.chunk_id
        title_counts[title] = title_counts.get(title, 0) + 1

    for item in sorted_items:
        if item.chunk_id in used_chunk_ids:
            continue
        title = item.chunk.title if item.chunk else item.chunk_id
        if title_counts.get(title, 0) >= 2:
            continue
        ranked.append(item.model_copy(update={"score": item.score - 0.2}))
        used_chunk_ids.add(item.chunk_id)
        title_counts[title] = title_counts.get(title, 0) + 1
        if len(ranked) >= top_k:
            break

    ranked.sort(key=lambda current: current.score, reverse=True)
    return ranked
