from __future__ import annotations

import math

from resumetailor_agent.config import AppConfig
from resumetailor_agent.embedding import build_local_embedding, cosine_similarity
from resumetailor_agent.nodes.query_planner import SYNONYM_MAP, build_query_plan, tokenize
from resumetailor_agent.schemas import EvidenceItem, JobRequirement, MaterialChunk, QueryPlan


def _document_frequency(chunks: list[MaterialChunk]) -> dict[str, int]:
    df: dict[str, int] = {}
    for chunk in chunks:
        searchable = f"{chunk.title} {chunk.raw_text} {' '.join(chunk.tags)}"
        unique_tokens = set(tokenize(searchable))
        for token in unique_tokens:
            df[token] = df.get(token, 0) + 1
    return df


def _score_chunk(
    query_plan: QueryPlan,
    chunk: MaterialChunk,
    document_frequency: dict[str, int],
    total_docs: int,
    config: AppConfig,
) -> tuple[float, list[str]]:
    searchable = f"{chunk.title} {chunk.raw_text} {' '.join(chunk.tags)}".lower()
    title_text = chunk.title.lower()
    chunk_tokens = tokenize(searchable)
    chunk_token_set = set(chunk_tokens)
    reasons: list[str] = []
    score = 0.0

    for keyword in query_plan.keywords:
        variants = SYNONYM_MAP.get(keyword, (keyword.lower(),))
        if any(variant.lower() in searchable for variant in variants):
            keyword_bonus = 2.0 if any(variant.lower() in title_text for variant in variants) else 1.5
            score += keyword_bonus
            reasons.append(f"Matches keyword: {keyword}")

    token_hits: list[str] = []
    for token in query_plan.query_tokens:
        if token not in chunk_token_set:
            continue
        idf = math.log((1 + total_docs) / (1 + document_frequency.get(token, 0))) + 1.0
        score += 0.35 * idf
        if token not in token_hits:
            token_hits.append(token)

    if token_hits:
        reasons.append(f"Overlapping terms: {', '.join(token_hits[:5])}")

    if config.retrieval_mode in {"hybrid", "vector"}:
        query_vector = build_local_embedding(query_plan.query_text, dimensions=config.embedding_dimensions)
        chunk_vector = build_local_embedding(searchable, dimensions=config.embedding_dimensions)
        vector_score = cosine_similarity(query_vector, chunk_vector)
        score += 0.9 * vector_score
        reasons.append(f"Vector score: {vector_score:.2f}")

    return score, reasons


def retrieve_relevant_chunks(
    requirement: JobRequirement,
    chunks: list[MaterialChunk],
    top_k: int = 5,
    config: AppConfig | None = None,
    query_plan: QueryPlan | None = None,
) -> list[EvidenceItem]:
    scored: list[EvidenceItem] = []
    config = config or AppConfig()
    query_plan = query_plan or build_query_plan(requirement)
    document_frequency = _document_frequency(chunks)
    total_docs = max(len(chunks), 1)

    for chunk in chunks:
        score, reasons = _score_chunk(
            query_plan=query_plan,
            chunk=chunk,
            document_frequency=document_frequency,
            total_docs=total_docs,
            config=config,
        )
        if score <= 0:
            continue
        scored.append(
            EvidenceItem(
                chunk_id=chunk.id,
                score=score,
                reason="; ".join(reasons),
                chunk=chunk,
            )
        )

    scored.sort(key=lambda item: item.score, reverse=True)
    return scored[:top_k]
