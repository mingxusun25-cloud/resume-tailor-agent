from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class JobRequirement(BaseModel):
    job_title: str = ""
    keywords: list[str] = Field(default_factory=list)
    must_have: list[str] = Field(default_factory=list)
    nice_to_have: list[str] = Field(default_factory=list)
    business_context: list[str] = Field(default_factory=list)
    target_level: str = ""
    resume_focus: list[str] = Field(default_factory=list)


class MaterialChunk(BaseModel):
    id: str
    title: str
    type: str
    source_file: str
    raw_text: str
    tags: list[str] = Field(default_factory=list)
    summary: str = ""


class EvidenceItem(BaseModel):
    chunk_id: str
    score: float
    reason: str
    chunk: MaterialChunk | None = None


class QueryPlan(BaseModel):
    keywords: list[str] = Field(default_factory=list)
    query_tokens: list[str] = Field(default_factory=list)
    expanded_terms: list[str] = Field(default_factory=list)
    query_text: str = ""


class RunContext(BaseModel):
    jd_raw: str
    jd_parsed: JobRequirement = Field(default_factory=JobRequirement)
    query_plan: QueryPlan = Field(default_factory=QueryPlan)
    retrieved_chunks: list[MaterialChunk] = Field(default_factory=list)
    ranked_evidence: list[EvidenceItem] = Field(default_factory=list)
    resume_output: dict[str, Any] = Field(default_factory=dict)
    interview_output: dict[str, Any] = Field(default_factory=dict)
    gap_output: dict[str, Any] = Field(default_factory=dict)
    review_output: dict[str, Any] = Field(default_factory=dict)
    export_path: str = ""
    run_log_path: str = ""


class ComparisonContext(BaseModel):
    run_id: str
    runs: list[RunContext] = Field(default_factory=list)
    summary: dict[str, Any] = Field(default_factory=dict)
    export_path: str = ""
