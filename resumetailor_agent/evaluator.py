from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field

from resumetailor_agent.config import AppConfig
from resumetailor_agent.exporter import export_evaluation_report, export_run_log
from resumetailor_agent.workflow import run_resume_tailor


class EvaluationCase(BaseModel):
    label: str
    jd_text: str = ""
    jd_file: str = ""
    materials_dir: str
    expected_keywords: list[str] = Field(default_factory=list)
    expected_projects: list[str] = Field(default_factory=list)


class EvaluationReport(BaseModel):
    run_id: str
    cases: list[dict[str, object]] = Field(default_factory=list)
    summary: dict[str, object] = Field(default_factory=dict)
    report_path: str = ""
    log_path: str = ""


def _resolve_case_path(base_dir: Path, raw_path: str) -> Path:
    path = Path(raw_path)
    if path.is_absolute():
        return path
    return (base_dir / path).resolve()


def _load_cases(cases_file: Path) -> list[EvaluationCase]:
    payload = json.loads(cases_file.read_text(encoding="utf-8"))
    return [EvaluationCase.model_validate(item) for item in payload]


def _load_case_jd(case: EvaluationCase, base_dir: Path) -> str:
    if case.jd_text:
        return case.jd_text
    if case.jd_file:
        return _resolve_case_path(base_dir, case.jd_file).read_text(encoding="utf-8")
    raise ValueError(f"Evaluation case '{case.label}' must provide jd_text or jd_file.")


def _compute_case_metrics(
    case: EvaluationCase,
    matched_keywords: list[str],
    project_highlights: list[str],
    evidence_count: int,
    risk_level: str,
) -> dict[str, object]:
    expected_keywords = case.expected_keywords
    expected_projects = case.expected_projects
    matched_keyword_set = set(matched_keywords)
    highlight_blob = "\n".join(project_highlights).lower()

    keyword_recall = 1.0
    if expected_keywords:
        keyword_recall = sum(1 for item in expected_keywords if item in matched_keyword_set) / len(
            expected_keywords
        )

    project_hit = 1.0
    if expected_projects:
        project_hit = sum(1 for item in expected_projects if item.lower() in highlight_blob) / len(
            expected_projects
        )

    evidence_presence = 1.0 if evidence_count > 0 else 0.0
    risk_score = {"low": 1.0, "medium": 0.6, "high": 0.2}.get(risk_level, 0.0)
    overall_score = round((keyword_recall + project_hit + evidence_presence + risk_score) / 4, 4)

    return {
        "keyword_recall": round(keyword_recall, 4),
        "project_hit": round(project_hit, 4),
        "evidence_presence": evidence_presence,
        "risk_score": risk_score,
        "overall_score": overall_score,
    }


def evaluate_cases_file(
    cases_file: Path,
    output_dir: Path,
    run_id: str = "quality-eval",
    config: AppConfig | None = None,
) -> EvaluationReport:
    config = config or AppConfig.from_env()
    base_dir = cases_file.parent
    cases = _load_cases(cases_file)
    case_rows: list[dict[str, object]] = []

    for index, case in enumerate(cases, start=1):
        jd_text = _load_case_jd(case, base_dir)
        materials_dir = _resolve_case_path(base_dir, case.materials_dir)
        case_run_id = f"{run_id}-{index}"
        run = run_resume_tailor(
            jd_text=jd_text,
            materials_dir=materials_dir,
            output_dir=output_dir,
            run_id=case_run_id,
            config=config,
        )
        highlights = [
            item for item in run.resume_output.get("project_highlights", []) if isinstance(item, str)
        ]
        metrics = _compute_case_metrics(
            case=case,
            matched_keywords=run.gap_output.get("matched_keywords", []),
            project_highlights=highlights,
            evidence_count=len(run.ranked_evidence),
            risk_level=run.review_output.get("risk_level", "unknown"),
        )
        case_rows.append(
            {
                "label": case.label,
                "expected_keywords": case.expected_keywords,
                "matched_keywords": run.gap_output.get("matched_keywords", []),
                "missing_keywords": run.gap_output.get("missing_keywords", []),
                "risk_level": run.review_output.get("risk_level", "unknown"),
                "report_path": run.export_path,
                **metrics,
            }
        )

    case_count = len(case_rows)
    average_keyword_recall = (
        round(sum(float(item["keyword_recall"]) for item in case_rows) / case_count, 4) if case_count else 0.0
    )
    average_project_hit = (
        round(sum(float(item["project_hit"]) for item in case_rows) / case_count, 4) if case_count else 0.0
    )
    average_overall_score = (
        round(sum(float(item["overall_score"]) for item in case_rows) / case_count, 4) if case_count else 0.0
    )
    summary = {
        "case_count": case_count,
        "average_keyword_recall": average_keyword_recall,
        "average_project_hit": average_project_hit,
        "average_overall_score": average_overall_score,
    }

    report_path = export_evaluation_report(
        output_dir=output_dir,
        run_id=run_id,
        summary=summary,
        case_rows=case_rows,
    )
    log_path = export_run_log(
        output_dir=output_dir,
        run_id=f"{run_id}-evaluation",
        payload={"cases": case_rows, "summary": summary},
    )
    return EvaluationReport(
        run_id=run_id,
        cases=case_rows,
        summary=summary,
        report_path=str(report_path),
        log_path=str(log_path),
    )
