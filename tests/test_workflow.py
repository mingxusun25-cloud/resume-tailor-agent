from pathlib import Path

from resumetailor_agent.config import AppConfig
from resumetailor_agent.workflow import run_resume_tailor, run_resume_tailor_compare


def test_run_resume_tailor_returns_exported_markdown(tmp_path: Path):
    materials_dir = tmp_path / "materials"
    materials_dir.mkdir()
    (materials_dir / "agent.md").write_text(
        "# Agent Daily\n\nBuilt a Python Agent automation workflow for GitHub trending reports.\n",
        encoding="utf-8",
    )

    result = run_resume_tailor(
        jd_text="AI应用实习生，要求 Python、Agent、自动化项目经验。",
        materials_dir=materials_dir,
        output_dir=tmp_path / "outputs",
        run_id="demo-run",
    )

    assert Path(result.export_path).exists()
    assert result.ranked_evidence
    assert result.resume_output["project_highlights"]


def test_run_resume_tailor_populates_interview_output(tmp_path: Path):
    materials_dir = tmp_path / "materials"
    materials_dir.mkdir()
    (materials_dir / "agent.md").write_text(
        "# Agent Daily\n\nBuilt a Python Agent automation workflow for GitHub trending reports.\n",
        encoding="utf-8",
    )

    result = run_resume_tailor(
        jd_text="AI应用实习生，要求 Python、Agent、自动化项目经验。",
        materials_dir=materials_dir,
        output_dir=tmp_path / "outputs",
        run_id="demo-run",
    )

    assert result.interview_output["questions"]


def test_run_resume_tailor_writes_json_run_log(tmp_path: Path):
    materials_dir = tmp_path / "materials"
    materials_dir.mkdir()
    (materials_dir / "agent.md").write_text(
        "# Agent Daily\n\nBuilt a Python Agent automation workflow for GitHub trending reports.\n",
        encoding="utf-8",
    )

    result = run_resume_tailor(
        jd_text="AI应用实习生，要求 Python、Agent、自动化项目经验。",
        materials_dir=materials_dir,
        output_dir=tmp_path / "outputs",
        run_id="demo-run",
    )

    log_path = Path(result.run_log_path)

    assert log_path.exists()
    assert log_path.suffix == ".json"
    log_content = log_path.read_text(encoding="utf-8")
    assert str(result.export_path) in log_content
    assert str(result.run_log_path) in log_content


def test_run_resume_tailor_records_mode_in_review_output(tmp_path: Path):
    materials_dir = tmp_path / "materials"
    materials_dir.mkdir()
    (materials_dir / "agent.md").write_text(
        "# Agent Daily\n\nBuilt a Python Agent automation workflow for GitHub trending reports.\n",
        encoding="utf-8",
    )

    result = run_resume_tailor(
        jd_text="AI应用实习生，要求 Python、Agent、自动化项目经验。",
        materials_dir=materials_dir,
        output_dir=tmp_path / "outputs",
        run_id="demo-run",
        config=AppConfig(),
    )

    assert result.review_output["mode"] == "rule"
    assert "python" in result.query_plan.query_tokens
    assert result.query_plan.query_text
    assert result.review_output["review_layers"] == ["rule"]
    assert result.review_output["model_review"]["enabled"] is False


def test_run_resume_tailor_returns_diverse_project_highlights(tmp_path: Path):
    materials_dir = tmp_path / "materials"
    materials_dir.mkdir()
    (materials_dir / "agent.md").write_text(
        "# GitHub Agent Daily\n\nBuilt a Python Agent automation workflow.\n\nImplemented markdown export and evidence organization.\n",
        encoding="utf-8",
    )
    (materials_dir / "resume.md").write_text(
        "# ResumeTailor Agent\n\nUsed Streamlit to expose matched evidence and review results.\n",
        encoding="utf-8",
    )

    result = run_resume_tailor(
        jd_text="AI应用实习生，要求 Python、Agent、自动化项目经验，优先考虑 Streamlit 项目经验。",
        materials_dir=materials_dir,
        output_dir=tmp_path / "outputs",
        run_id="diverse-run",
        config=AppConfig(),
    )

    assert len(result.resume_output["project_highlights"]) == 2
    assert "GitHub Agent Daily" in result.resume_output["project_highlights"][0]
    assert any("ResumeTailor Agent" in item for item in result.resume_output["project_highlights"])


def test_run_resume_tailor_populates_gap_analysis(tmp_path: Path):
    materials_dir = tmp_path / "materials"
    materials_dir.mkdir()
    (materials_dir / "agent.md").write_text(
        "# Agent Daily\n\nBuilt a Python Agent automation workflow for GitHub trending reports.\n",
        encoding="utf-8",
    )

    result = run_resume_tailor(
        jd_text="AI应用实习生，要求 Python、Agent、RAG 项目经验。",
        materials_dir=materials_dir,
        output_dir=tmp_path / "outputs",
        run_id="gap-run",
        config=AppConfig(),
    )

    assert result.gap_output["matched_keywords"] == ["Python", "Agent"]
    assert result.gap_output["missing_keywords"] == ["RAG"]
    assert result.gap_output["gap_level"] == "medium"


def test_run_resume_tailor_returns_structured_gap_suggestions(tmp_path: Path):
    materials_dir = tmp_path / "materials"
    materials_dir.mkdir()
    (materials_dir / "agent.md").write_text(
        "# Agent Daily\n\nBuilt a Python Agent automation workflow.\n",
        encoding="utf-8",
    )

    result = run_resume_tailor(
        jd_text="AI应用实习生，要求 Python、RAG 项目经验。",
        materials_dir=materials_dir,
        output_dir=tmp_path / "outputs",
        run_id="gap-structured",
        config=AppConfig(),
    )

    first = result.gap_output["suggestion_cards"][0]

    assert first["keyword"] == "RAG"
    assert first["action"]


def test_run_resume_tailor_compare_generates_summary_report(tmp_path: Path):
    materials_dir = tmp_path / "materials"
    materials_dir.mkdir()
    (materials_dir / "agent.md").write_text(
        "# Agent Daily\n\nBuilt a Python Agent automation workflow for GitHub trending reports.\n",
        encoding="utf-8",
    )
    (materials_dir / "streamlit.md").write_text(
        "# ResumeTailor Agent\n\nUsed Streamlit to expose matched evidence and review results.\n",
        encoding="utf-8",
    )

    comparison = run_resume_tailor_compare(
        jd_inputs=[
            ("AI应用", "AI应用实习生，要求 Python、Agent、自动化项目经验。"),
            ("演示岗", "AI应用实习生，要求 Streamlit、Python 项目经验。"),
        ],
        materials_dir=materials_dir,
        output_dir=tmp_path / "outputs",
        run_id="compare-run",
        config=AppConfig(),
    )

    assert Path(comparison.export_path).exists()
    assert len(comparison.runs) == 2
    assert comparison.summary["common_keywords"] == ["Python"]
    assert comparison.summary["comparison_rows"][1]["missing_keywords"] == []
    assert comparison.summary["comparison_rows"][0]["unique_keywords"] == ["Agent", "自动化"]
    assert comparison.summary["comparison_rows"][1]["unique_keywords"] == ["Streamlit"]
