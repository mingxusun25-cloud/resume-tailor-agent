# ResumeTailor Agent V1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first runnable vertical slice of ResumeTailor Agent V1, covering material loading, JD parsing, evidence retrieval, resume generation, review, and Markdown export.

**Architecture:** Use a lightweight Python package with a node-based workflow orchestrator. Keep the first version deterministic where possible so the system is testable without a live model, while leaving clear seams for later LLM and vector-store integration.

**Tech Stack:** Python 3.11, pytest, Streamlit, Pydantic, Markdown/JSON local files

---

### Task 1: Project Skeleton and Shared Schemas

**Files:**
- Create: `resumetailor_agent/__init__.py`
- Create: `resumetailor_agent/schemas.py`
- Create: `tests/test_schemas.py`

- [ ] **Step 1: Write the failing test**

```python
from resumetailor_agent.schemas import JobRequirement, MaterialChunk, RunContext


def test_run_context_starts_with_empty_workflow_state():
    context = RunContext(jd_raw="Need Python and Agent workflow experience")

    assert context.jd_raw.startswith("Need Python")
    assert context.retrieved_chunks == []
    assert context.ranked_evidence == []
    assert context.resume_output == {}
    assert context.review_output == {}


def test_material_chunk_keeps_core_metadata():
    chunk = MaterialChunk(
        id="exp-1",
        title="GitHub Agent Daily",
        type="project",
        source_file="materials/github-agent.md",
        raw_text="Built a Python workflow that collected GitHub Agent projects.",
        tags=["Python", "Agent"],
    )

    assert chunk.title == "GitHub Agent Daily"
    assert chunk.tags == ["Python", "Agent"]


def test_job_requirement_defaults_lists():
    requirement = JobRequirement()

    assert requirement.keywords == []
    assert requirement.must_have == []
    assert requirement.resume_focus == []
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_schemas.py -v`
Expected: FAIL with `ModuleNotFoundError` for `resumetailor_agent`

- [ ] **Step 3: Write minimal implementation**

Create `resumetailor_agent/__init__.py` and `resumetailor_agent/schemas.py` with Pydantic models for `JobRequirement`, `MaterialChunk`, `EvidenceItem`, `GeneratedSection`, and `RunContext`.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_schemas.py -v`
Expected: PASS

### Task 2: Material Loading and Chunking

**Files:**
- Create: `resumetailor_agent/materials.py`
- Create: `tests/test_materials.py`

- [ ] **Step 1: Write the failing test**

```python
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_materials.py -v`
Expected: FAIL with `ModuleNotFoundError` or missing function

- [ ] **Step 3: Write minimal implementation**

Create a Markdown loader that:
- Reads `.md`, `.txt`, and `.json`
- Uses the first Markdown heading as title when available
- Creates one `MaterialChunk` per file for V1

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_materials.py -v`
Expected: PASS

### Task 3: JD Parser and Retrieval

**Files:**
- Create: `resumetailor_agent/nodes/jd_parser.py`
- Create: `resumetailor_agent/nodes/retriever.py`
- Create: `tests/test_jd_parser.py`
- Create: `tests/test_retriever.py`

- [ ] **Step 1: Write the failing tests**

```python
from resumetailor_agent.nodes.jd_parser import parse_job_description


def test_parse_job_description_extracts_keywords_and_must_have():
    jd = "AI应用实习生，要求熟悉 Python、RAG、Agent 工作流，有自动化项目经验。"

    parsed = parse_job_description(jd)

    assert "Python" in parsed.keywords
    assert "RAG" in parsed.keywords
    assert any("自动化" in item for item in parsed.must_have)
```

```python
from resumetailor_agent.nodes.retriever import retrieve_relevant_chunks
from resumetailor_agent.schemas import JobRequirement, MaterialChunk


def test_retrieve_relevant_chunks_prefers_keyword_overlap():
    requirement = JobRequirement(keywords=["Python", "Agent", "自动化"])
    chunks = [
        MaterialChunk(
            id="1",
            title="Agent Daily",
            type="project",
            source_file="a.md",
            raw_text="Built a Python Agent automation workflow for GitHub trending reports.",
            tags=["Python", "Agent", "automation"],
        ),
        MaterialChunk(
            id="2",
            title="Antenna Simulation",
            type="project",
            source_file="b.md",
            raw_text="Completed antenna modeling and simulation experiments.",
            tags=["HFSS"],
        ),
    ]

    results = retrieve_relevant_chunks(requirement, chunks, top_k=1)

    assert len(results) == 1
    assert results[0].chunk_id == "1"
    assert results[0].score > 0
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_jd_parser.py tests/test_retriever.py -v`
Expected: FAIL because parser and retriever are not implemented

- [ ] **Step 3: Write minimal implementation**

Implement:
- A rule-based parser with a normalized keyword vocabulary
- A simple overlap-based scoring retriever with tag and text matching

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_jd_parser.py tests/test_retriever.py -v`
Expected: PASS

### Task 4: Resume Generation, Review, and Export

**Files:**
- Create: `resumetailor_agent/nodes/resume_writer.py`
- Create: `resumetailor_agent/nodes/reviewer.py`
- Create: `resumetailor_agent/exporter.py`
- Create: `tests/test_resume_writer.py`
- Create: `tests/test_reviewer.py`
- Create: `tests/test_exporter.py`

- [ ] **Step 1: Write the failing tests**

```python
from resumetailor_agent.nodes.resume_writer import build_resume_output
from resumetailor_agent.schemas import EvidenceItem, JobRequirement, MaterialChunk


def test_build_resume_output_uses_evidence_titles_and_keywords():
    requirement = JobRequirement(keywords=["Python", "Agent"], must_have=["自动化项目经验"])
    chunk = MaterialChunk(
        id="1",
        title="Agent Daily",
        type="project",
        source_file="a.md",
        raw_text="Built a Python Agent automation workflow for GitHub trending reports.",
        tags=["Python", "Agent"],
    )
    evidence = [EvidenceItem(chunk_id="1", score=3.0, reason="Matches Python and Agent keywords", chunk=chunk)]

    output = build_resume_output(requirement, evidence)

    assert "Agent Daily" in output["project_highlights"][0]
    assert "Python" in output["skills_summary"]
```

```python
from resumetailor_agent.nodes.reviewer import review_resume_output


def test_review_resume_output_flags_unbacked_claims():
    resume_output = {
        "project_highlights": ["Led large-scale LLM platform architecture independently."],
        "skills_summary": "Expert in distributed systems and deep learning infrastructure.",
    }
    evidence_texts = ["Built a Python script for GitHub project tracking."]

    review = review_resume_output(resume_output, evidence_texts)

    assert review["risk_level"] in {"medium", "high"}
    assert review["issues"]
```

```python
from pathlib import Path

from resumetailor_agent.exporter import export_markdown_report


def test_export_markdown_report_creates_readable_file(tmp_path: Path):
    output_path = export_markdown_report(
        tmp_path,
        "test-run",
        {"keywords": ["Python", "Agent"]},
        ["Agent Daily: matched Python and Agent"],
        {"project_highlights": ["Built an Agent workflow"], "skills_summary": "Python, Agent"},
        {"risk_level": "low", "issues": []},
    )

    content = output_path.read_text(encoding="utf-8")

    assert output_path.exists()
    assert "# 岗位 JD 定制结果" in content
    assert "Built an Agent workflow" in content
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `pytest tests/test_resume_writer.py tests/test_reviewer.py tests/test_exporter.py -v`
Expected: FAIL because modules are missing

- [ ] **Step 3: Write minimal implementation**

Implement:
- Resume output builder from evidence
- Rule-based reviewer for risky claims
- Markdown exporter with fixed section layout

- [ ] **Step 4: Run tests to verify they pass**

Run: `pytest tests/test_resume_writer.py tests/test_reviewer.py tests/test_exporter.py -v`
Expected: PASS

### Task 5: Workflow Runner and Streamlit Entrypoint

**Files:**
- Create: `resumetailor_agent/workflow.py`
- Create: `streamlit_app.py`
- Create: `sample_materials/github_agent_daily.md`
- Create: `tests/test_workflow.py`

- [ ] **Step 1: Write the failing test**

```python
from pathlib import Path

from resumetailor_agent.workflow import run_resume_tailor


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

    assert result.export_path.exists()
    assert result.ranked_evidence
    assert result.resume_output["project_highlights"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_workflow.py -v`
Expected: FAIL because workflow runner is missing

- [ ] **Step 3: Write minimal implementation**

Implement:
- End-to-end orchestration function
- Streamlit app with JD input, materials path input, and result rendering
- A sample material file for local testing

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_workflow.py -v`
Expected: PASS

### Task 6: Full Verification

**Files:**
- Verify: `tests/`

- [ ] **Step 1: Run the full test suite**

Run: `pytest -q`
Expected: all tests pass

- [ ] **Step 2: Smoke-check the app entrypoint**

Run: `python3 -c "from resumetailor_agent.workflow import run_resume_tailor; print('ok')"`
Expected: `ok`

- [ ] **Step 3: Optional manual UI check**

Run: `streamlit run streamlit_app.py`
Expected: local Streamlit app starts without import errors
