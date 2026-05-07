# ResumeTailor Agent V1.1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade the current skeleton into a more faithful V1 system by adding finer-grained evidence chunks, interview-question generation, and richer exported/UI output.

**Architecture:** Keep the deterministic local workflow, but improve the quality of its intermediate artifacts. Split material files into paragraph-level chunks, generate interview follow-up questions from evidence-backed resume output, and expose those new artifacts in the workflow result, Markdown export, and Streamlit UI.

**Tech Stack:** Python 3.11, pytest, Streamlit, Pydantic, Markdown/JSON local files

---

### Task 1: Paragraph-Level Material Chunking

**Files:**
- Modify: `resumetailor_agent/materials.py`
- Modify: `tests/test_materials.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path

from resumetailor_agent.materials import load_material_chunks


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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_materials.py::test_load_material_chunks_splits_markdown_into_multiple_paragraph_chunks -v`
Expected: FAIL because the loader currently returns one chunk per file

- [ ] **Step 3: Write minimal implementation**

Update `resumetailor_agent/materials.py` so Markdown and text files:
- Ignore the heading line for body chunking
- Split body text on blank lines
- Create one `MaterialChunk` per non-empty paragraph
- Suffix chunk IDs with an index like `agent_project-1`

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_materials.py::test_load_material_chunks_splits_markdown_into_multiple_paragraph_chunks -v`
Expected: PASS

### Task 2: Interview Question Generation

**Files:**
- Create: `resumetailor_agent/nodes/interview_generator.py`
- Modify: `resumetailor_agent/workflow.py`
- Modify: `tests/test_workflow.py`
- Create: `tests/test_interview_generator.py`

- [ ] **Step 1: Write the failing tests**

```python
from resumetailor_agent.nodes.interview_generator import build_interview_output


def test_build_interview_output_generates_questions_from_project_highlights():
    resume_output = {
        "project_highlights": [
            "Agent Daily: Built a Python Agent automation workflow for GitHub trending reports."
        ],
        "skills_summary": "Python, Agent, 自动化",
    }

    interview_output = build_interview_output(resume_output)

    assert interview_output["questions"]
    assert "Agent Daily" in interview_output["questions"][0]["question"]
```

```python
from pathlib import Path

from resumetailor_agent.workflow import run_resume_tailor


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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_interview_generator.py tests/test_workflow.py::test_run_resume_tailor_populates_interview_output -v`
Expected: FAIL because there is no interview generator node and workflow does not populate interview output

- [ ] **Step 3: Write minimal implementation**

Create `build_interview_output` that:
- Reads `project_highlights`
- Produces 2-3 evidence-linked follow-up questions
- Includes a short answer hint per question

Update `run_resume_tailor` to store `context.interview_output`.

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_interview_generator.py tests/test_workflow.py::test_run_resume_tailor_populates_interview_output -v`
Expected: PASS

### Task 3: Richer Markdown Export and UI Rendering

**Files:**
- Modify: `resumetailor_agent/exporter.py`
- Modify: `streamlit_app.py`
- Modify: `tests/test_exporter.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path

from resumetailor_agent.exporter import export_markdown_report


def test_export_markdown_report_includes_interview_questions(tmp_path: Path):
    output_path = export_markdown_report(
        tmp_path,
        "test-run",
        {"keywords": ["Python", "Agent"]},
        ["Agent Daily: matched Python and Agent"],
        {"project_highlights": ["Built an Agent workflow"], "skills_summary": "Python, Agent"},
        {"questions": [{"question": "How did Agent Daily use Python?", "hint": "Explain retrieval and export flow."}]},
        {"risk_level": "low", "issues": []},
    )

    content = output_path.read_text(encoding="utf-8")

    assert "## 6. 面试高频追问" in content
    assert "How did Agent Daily use Python?" in content
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_exporter.py::test_export_markdown_report_includes_interview_questions -v`
Expected: FAIL because exporter does not accept or render interview output

- [ ] **Step 3: Write minimal implementation**

Update `export_markdown_report` to:
- Accept `interview_output`
- Render a `面试高频追问` section before the risk section

Update `streamlit_app.py` to:
- Show interview questions in the right column
- Show the first chunk text for each evidence item for easier inspection

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_exporter.py::test_export_markdown_report_includes_interview_questions -v`
Expected: PASS

### Task 4: Full Verification

**Files:**
- Verify: `tests/`

- [ ] **Step 1: Run the full test suite**

Run: `pytest -q`
Expected: all tests pass

- [ ] **Step 2: Smoke-check the workflow with sample materials**

Run: `/Users/smx/.pyenv/versions/3.11.8/bin/python3.11 -c "from resumetailor_agent.workflow import run_resume_tailor; from pathlib import Path; result = run_resume_tailor('AI应用实习生，要求 Python、Agent、自动化项目经验。', Path('sample_materials'), Path('outputs'), 'v1-1-run'); print(result.export_path); print(bool(result.interview_output.get('questions')))"` 
Expected: exported Markdown path printed and `True`

- [ ] **Step 3: Smoke-check the Streamlit entrypoint import**

Run: `/Users/smx/.pyenv/versions/3.11.8/bin/python3.11 -c "import streamlit_app; print('streamlit-app-ok')"`
Expected: `streamlit-app-ok`
