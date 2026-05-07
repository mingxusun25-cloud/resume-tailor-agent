import json
from pathlib import Path

from resumetailor_agent.config import AppConfig
from resumetailor_agent.evaluator import evaluate_cases_file


def test_evaluate_cases_file_generates_quality_report(tmp_path: Path):
    materials_dir = tmp_path / "materials"
    materials_dir.mkdir()
    (materials_dir / "agent.md").write_text(
        "# Agent Daily\n\nBuilt a Python Agent automation workflow for GitHub trending reports.\n",
        encoding="utf-8",
    )
    jd_file = tmp_path / "jd.md"
    jd_file.write_text("AI应用实习生，要求 Python、Agent、自动化项目经验。", encoding="utf-8")
    cases_file = tmp_path / "cases.json"
    cases_file.write_text(
        json.dumps(
            [
                {
                    "label": "agent-case",
                    "jd_file": "jd.md",
                    "materials_dir": "materials",
                    "expected_keywords": ["Python", "Agent"],
                    "expected_projects": ["Agent Daily"],
                }
            ],
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    report = evaluate_cases_file(
        cases_file=cases_file,
        output_dir=tmp_path / "outputs",
        run_id="quality-eval",
        config=AppConfig(),
    )

    assert report.summary["case_count"] == 1
    assert report.summary["average_keyword_recall"] == 1.0
    assert report.cases[0]["project_hit"] == 1.0
    assert Path(report.report_path).exists()
