from __future__ import annotations

from pathlib import Path
import re

from resumetailor_agent.config import AppConfig
from resumetailor_agent.exporter import (
    export_comparison_report,
    export_markdown_report,
    export_run_log,
)
from resumetailor_agent.llm import enhance_resume_output
from resumetailor_agent.nodes.evidence_ranker import rank_evidence_items
from resumetailor_agent.nodes.gap_analyzer import build_gap_output
from resumetailor_agent.materials import load_material_chunks
from resumetailor_agent.nodes.interview_generator import build_interview_output
from resumetailor_agent.nodes.jd_parser import parse_job_description
from resumetailor_agent.nodes.query_planner import build_query_plan
from resumetailor_agent.nodes.resume_writer import build_resume_output
from resumetailor_agent.nodes.retriever import retrieve_relevant_chunks
from resumetailor_agent.nodes.reviewer import review_resume_output
from resumetailor_agent.schemas import ComparisonContext, RunContext


def run_resume_tailor(
    jd_text: str,
    materials_dir: Path,
    output_dir: Path,
    run_id: str = "latest-run",
    config: AppConfig | None = None,
) -> RunContext:
    config = config or AppConfig.from_env()
    context = RunContext(jd_raw=jd_text)
    context.jd_parsed = parse_job_description(jd_text)
    context.query_plan = build_query_plan(context.jd_parsed)
    context.retrieved_chunks = load_material_chunks(materials_dir)
    retrieved_evidence = retrieve_relevant_chunks(
        context.jd_parsed,
        context.retrieved_chunks,
        config=config,
        query_plan=context.query_plan,
    )
    context.ranked_evidence = rank_evidence_items(context.jd_parsed, retrieved_evidence)
    context.resume_output = build_resume_output(context.jd_parsed, context.ranked_evidence)
    evidence_lines = [
        f"{item.chunk.title if item.chunk else item.chunk_id}: {item.reason}"
        for item in context.ranked_evidence
    ]
    context.resume_output = enhance_resume_output(
        config=config,
        resume_output=context.resume_output,
        jd_summary=context.jd_parsed.model_dump(),
        evidence_lines=evidence_lines,
    )
    context.interview_output = build_interview_output(context.resume_output)
    context.gap_output = build_gap_output(context.jd_parsed, context.ranked_evidence)
    evidence_texts = [item.chunk.raw_text for item in context.ranked_evidence if item.chunk]
    context.review_output = review_resume_output(
        context.resume_output,
        evidence_texts,
        mode=config.mode,
        config=config,
    )
    export_path = export_markdown_report(
        output_dir=output_dir,
        run_id=run_id,
        jd_summary=context.jd_parsed.model_dump(),
        evidence_lines=evidence_lines,
        resume_output=context.resume_output,
        interview_output=context.interview_output,
        review_output=context.review_output,
        gap_output=context.gap_output,
        query_plan=context.query_plan.model_dump(),
    )
    context.export_path = str(export_path)
    context.run_log_path = str(output_dir / f"{run_id}.json")
    run_log_path = export_run_log(output_dir=output_dir, run_id=run_id, payload=context.model_dump())
    context.run_log_path = str(run_log_path)
    return context


def _slugify_label(label: str, index: int) -> str:
    cleaned = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", "-", label).strip("-").lower()
    return cleaned or f"jd-{index}"


def _build_comparison_summary(run_labels: list[str], runs: list[RunContext]) -> dict[str, object]:
    keyword_sets = [set(run.jd_parsed.keywords) for run in runs if run.jd_parsed.keywords]
    common_keywords = sorted(set.intersection(*keyword_sets)) if keyword_sets else []
    comparison_rows: list[dict[str, object]] = []

    for label, run in zip(run_labels, runs):
        top_project = ""
        project_highlights = run.resume_output.get("project_highlights", [])
        if isinstance(project_highlights, list) and project_highlights:
            first_item = project_highlights[0]
            if isinstance(first_item, str):
                top_project = first_item.split(":", 1)[0].strip()

        comparison_rows.append(
            {
                "label": label,
                "keywords": run.jd_parsed.keywords,
                "unique_keywords": sorted(set(run.jd_parsed.keywords) - set(common_keywords)),
                "top_project": top_project,
                "missing_keywords": run.gap_output.get("missing_keywords", []),
                "risk_level": run.review_output.get("risk_level", "unknown"),
                "export_path": run.export_path,
            }
        )

    return {"common_keywords": common_keywords, "comparison_rows": comparison_rows}


def run_resume_tailor_compare(
    jd_inputs: list[tuple[str, str]],
    materials_dir: Path,
    output_dir: Path,
    run_id: str = "compare-run",
    config: AppConfig | None = None,
) -> ComparisonContext:
    config = config or AppConfig.from_env()
    runs: list[RunContext] = []
    labels: list[str] = []

    for index, (label, jd_text) in enumerate(jd_inputs, start=1):
        labels.append(label)
        child_run_id = f"{run_id}-{_slugify_label(label, index)}"
        runs.append(
            run_resume_tailor(
                jd_text=jd_text,
                materials_dir=materials_dir,
                output_dir=output_dir,
                run_id=child_run_id,
                config=config,
            )
        )

    summary = _build_comparison_summary(labels, runs)
    export_path = export_comparison_report(output_dir=output_dir, run_id=run_id, summary=summary)
    return ComparisonContext(run_id=run_id, runs=runs, summary=summary, export_path=str(export_path))
