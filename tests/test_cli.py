from pathlib import Path

from resumetailor_agent.cli import main


def test_cli_main_creates_markdown_output(tmp_path: Path):
    materials_dir = tmp_path / "materials"
    materials_dir.mkdir()
    (materials_dir / "agent.md").write_text(
        "# Agent Daily\n\nBuilt a Python Agent automation workflow for GitHub trending reports.\n",
        encoding="utf-8",
    )

    output_dir = tmp_path / "outputs"
    exit_code = main(
        [
            "--jd-text",
            "AI应用实习生，要求 Python、Agent、自动化项目经验。",
            "--materials-dir",
            str(materials_dir),
            "--output-dir",
            str(output_dir),
            "--run-id",
            "cli-run",
        ]
    )

    assert exit_code == 0
    assert (output_dir / "cli-run.md").exists()


def test_cli_main_supports_multi_jd_comparison(tmp_path: Path):
    materials_dir = tmp_path / "materials"
    materials_dir.mkdir()
    (materials_dir / "agent.md").write_text(
        "# Agent Daily\n\nBuilt a Python Agent automation workflow for GitHub trending reports.\n",
        encoding="utf-8",
    )
    jd_one = tmp_path / "jd-one.md"
    jd_one.write_text("AI应用实习生，要求 Python、Agent、自动化项目经验。", encoding="utf-8")
    jd_two = tmp_path / "jd-two.md"
    jd_two.write_text("AI应用实习生，要求 Python、RAG 项目经验。", encoding="utf-8")

    output_dir = tmp_path / "outputs"
    exit_code = main(
        [
            "--compare-jd-files",
            str(jd_one),
            str(jd_two),
            "--materials-dir",
            str(materials_dir),
            "--output-dir",
            str(output_dir),
            "--run-id",
            "compare-run",
        ]
    )

    assert exit_code == 0
    assert (output_dir / "compare-run-comparison.md").exists()


def test_cli_main_supports_quality_evaluation(tmp_path: Path):
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
        (
            '[{"label":"agent-case","jd_file":"jd.md","materials_dir":"materials",'
            '"expected_keywords":["Python","Agent"],"expected_projects":["Agent Daily"]}]'
        ),
        encoding="utf-8",
    )

    output_dir = tmp_path / "outputs"
    exit_code = main(
        [
            "--eval-cases-file",
            str(cases_file),
            "--output-dir",
            str(output_dir),
            "--run-id",
            "quality-eval",
        ]
    )

    assert exit_code == 0
    assert (output_dir / "quality-eval-evaluation.md").exists()
