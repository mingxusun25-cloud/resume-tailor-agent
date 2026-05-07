from pathlib import Path

from resumetailor_agent.materials import load_material_chunks


def test_load_material_chunks_reads_markdown_files(tmp_path: Path):
    materials_dir = tmp_path / "materials"
    materials_dir.mkdir()
    (materials_dir / "agent_project.md").write_text(
        "# Agent Project\n\nBuilt a Python tool for JD-driven resume customization.\n",
        encoding="utf-8",
    )

    chunks = load_material_chunks(materials_dir)

    assert len(chunks) == 1
    assert chunks[0].title == "Agent Project"
    assert "Python tool" in chunks[0].raw_text
    assert chunks[0].source_file.endswith("agent_project.md")


def test_load_material_chunks_splits_markdown_into_multiple_paragraph_chunks(tmp_path: Path):
    materials_dir = tmp_path / "materials"
    materials_dir.mkdir()
    (materials_dir / "agent_project.md").write_text(
        "# Agent Project\n\nBuilt a Python tool for JD-driven resume customization.\n\nImplemented retrieval and markdown export.\n",
        encoding="utf-8",
    )

    chunks = load_material_chunks(materials_dir)

    assert len(chunks) == 2
    assert chunks[0].title == "Agent Project"
    assert "JD-driven" in chunks[0].raw_text
    assert "markdown export" in chunks[1].raw_text
    assert chunks[0].id != chunks[1].id
