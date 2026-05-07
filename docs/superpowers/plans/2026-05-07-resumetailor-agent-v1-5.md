# ResumeTailor Agent V1.5 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a practical V1.5 quality-upgrade slice covering vector-style retrieval, stronger constrained LLM merging, Streamlit multi-JD comparison, and finer-grained gap suggestions.

**Architecture:** Keep the current local deterministic workflow as the default path, then layer in lightweight enhancements that do not require heavy external infrastructure. Retrieval should become hybrid by combining the existing lexical scorer with a local dense-vector baseline, LLM enhancement should be merged through stricter schema and evidence constraints, and the UI should expose the already-existing comparison workflow instead of leaving it CLI-only.

**Tech Stack:** Python 3.11, pytest, Streamlit, Pydantic, local hashed embeddings, Markdown/JSON reports

---

### Task 1: Add Local Vector-Style Retrieval

**Files:**
- Create: `resumetailor_agent/embedding.py`
- Modify: `resumetailor_agent/config.py`
- Modify: `resumetailor_agent/nodes/retriever.py`
- Modify: `resumetailor_agent/workflow.py`
- Test: `tests/test_retriever.py`
- Test: `tests/test_config.py`

- [ ] **Step 1: Write the failing tests**

```python
from resumetailor_agent.config import AppConfig
from resumetailor_agent.nodes.retriever import retrieve_relevant_chunks
from resumetailor_agent.schemas import JobRequirement, MaterialChunk


def test_app_config_defaults_to_hybrid_retrieval():
    config = AppConfig()

    assert config.retrieval_mode == "hybrid"
    assert config.embedding_backend == "local"


def test_retrieve_relevant_chunks_reports_vector_signal():
    requirement = JobRequirement(keywords=["Python", "Agent"])
    chunks = [
        MaterialChunk(
            id="1",
            title="Agent Daily",
            type="project",
            source_file="a.md",
            raw_text="Built a Python Agent automation workflow.",
            tags=["Python", "Agent"],
        )
    ]

    results = retrieve_relevant_chunks(requirement, chunks, top_k=1, config=AppConfig())

    assert results[0].chunk_id == "1"
    assert "Vector score" in results[0].reason
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `/Users/smx/.pyenv/versions/3.11.8/bin/python3.11 -m pytest tests/test_config.py tests/test_retriever.py -v`
Expected: FAIL because `AppConfig` has no retrieval settings and `retrieve_relevant_chunks` has no vector signal support

- [ ] **Step 3: Write minimal implementation**

```python
# resumetailor_agent/embedding.py
from __future__ import annotations

import math

from resumetailor_agent.nodes.retriever import _tokenize


def build_local_embedding(text: str, dimensions: int = 64) -> list[float]:
    vector = [0.0] * dimensions
    for token in _tokenize(text):
        index = hash(token) % dimensions
        vector[index] += 1.0
    norm = math.sqrt(sum(value * value for value in vector))
    if norm:
        return [value / norm for value in vector]
    return vector
```

```python
# resumetailor_agent/config.py
class AppConfig(BaseModel):
    ...
    retrieval_mode: str = "hybrid"
    embedding_backend: str = "local"
    embedding_dimensions: int = 64
```

```python
# resumetailor_agent/nodes/retriever.py
def retrieve_relevant_chunks(
    requirement: JobRequirement,
    chunks: list[MaterialChunk],
    top_k: int = 5,
    config: AppConfig | None = None,
) -> list[EvidenceItem]:
    ...
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `/Users/smx/.pyenv/versions/3.11.8/bin/python3.11 -m pytest tests/test_config.py tests/test_retriever.py -v`
Expected: PASS

### Task 2: Strengthen LLM Constrained Merging

**Files:**
- Modify: `resumetailor_agent/llm.py`
- Test: `tests/test_llm.py`

- [ ] **Step 1: Write the failing tests**

```python
from resumetailor_agent.config import AppConfig
from resumetailor_agent.llm import _merge_constrained_resume_output


def test_merge_constrained_resume_output_discards_invalid_fields():
    draft = {
        "fit_summary": "rule summary",
        "project_highlights": ["Agent Daily: Built workflow."],
        "skills_summary": "Python, Agent",
        "self_intro": "候选人具备 Python 相关实践。",
        "matched_requirements": ["Matches keyword: Python"],
    }
    enhanced = {
        "fit_summary": "  stronger summary  ",
        "project_highlights": "not-a-list",
        "skills_summary": ["Python"],
        "self_intro": "new intro",
    }

    merged = _merge_constrained_resume_output(draft, enhanced)

    assert merged["fit_summary"] == "stronger summary"
    assert merged["project_highlights"] == draft["project_highlights"]
    assert merged["skills_summary"] == draft["skills_summary"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `/Users/smx/.pyenv/versions/3.11.8/bin/python3.11 -m pytest tests/test_llm.py -v`
Expected: FAIL because there is no constrained merge helper

- [ ] **Step 3: Write minimal implementation**

```python
def _merge_constrained_resume_output(
    resume_output: dict[str, object], enhanced: dict[str, object]
) -> dict[str, object]:
    merged = dict(resume_output)
    ...
    return merged
```

- [ ] **Step 4: Run test to verify it passes**

Run: `/Users/smx/.pyenv/versions/3.11.8/bin/python3.11 -m pytest tests/test_llm.py -v`
Expected: PASS

### Task 3: Improve Gap Suggestions

**Files:**
- Modify: `resumetailor_agent/nodes/gap_analyzer.py`
- Modify: `resumetailor_agent/exporter.py`
- Test: `tests/test_workflow.py`
- Test: `tests/test_exporter.py`

- [ ] **Step 1: Write the failing tests**

```python
from pathlib import Path

from resumetailor_agent.config import AppConfig
from resumetailor_agent.workflow import run_resume_tailor


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
```

- [ ] **Step 2: Run tests to verify they fail**

Run: `/Users/smx/.pyenv/versions/3.11.8/bin/python3.11 -m pytest tests/test_workflow.py tests/test_exporter.py -v`
Expected: FAIL because gap output has only plain string suggestions

- [ ] **Step 3: Write minimal implementation**

```python
SUGGESTION_LIBRARY = {
    "RAG": {
        "action": "补一段检索增强或知识库问答经历",
        "evidence_hint": "写清召回、排序、输出链路",
    }
}
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `/Users/smx/.pyenv/versions/3.11.8/bin/python3.11 -m pytest tests/test_workflow.py tests/test_exporter.py -v`
Expected: PASS

### Task 4: Expose Multi-JD Compare In Streamlit

**Files:**
- Create: `resumetailor_agent/ui_helpers.py`
- Modify: `streamlit_app.py`
- Test: `tests/test_workflow.py`

- [ ] **Step 1: Write the failing test**

```python
from resumetailor_agent.ui_helpers import parse_compare_inputs


def test_parse_compare_inputs_converts_labeled_blocks():
    pairs = parse_compare_inputs("AI应用::需要 Python\\n---\\n演示岗::需要 Streamlit")

    assert pairs == [("AI应用", "需要 Python"), ("演示岗", "需要 Streamlit")]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `/Users/smx/.pyenv/versions/3.11.8/bin/python3.11 -m pytest tests/test_workflow.py -v`
Expected: FAIL because the helper does not exist

- [ ] **Step 3: Write minimal implementation**

```python
def parse_compare_inputs(raw_text: str) -> list[tuple[str, str]]:
    ...
```

- [ ] **Step 4: Run test to verify it passes**

Run: `/Users/smx/.pyenv/versions/3.11.8/bin/python3.11 -m pytest tests/test_workflow.py -v`
Expected: PASS

### Task 5: Full Verification

**Files:**
- Verify: `tests/`
- Verify: `streamlit_app.py`

- [ ] **Step 1: Run the full test suite**

Run: `/Users/smx/.pyenv/versions/3.11.8/bin/python3.11 -m pytest -q`
Expected: all tests pass

- [ ] **Step 2: Smoke-check comparison workflow**

Run: `/Users/smx/.pyenv/versions/3.11.8/bin/python3.11 -c "from pathlib import Path; from resumetailor_agent.workflow import run_resume_tailor_compare; result = run_resume_tailor_compare([('agent','AI应用实习生，要求 Python、Agent、自动化项目经验。'),('rag','AI应用实习生，要求 Python、RAG 项目经验。')], Path('sample_materials'), Path('outputs'), 'v1-5-smoke'); print(result.export_path); print(result.summary['common_keywords'])"`
Expected: comparison Markdown path printed and a list containing `Python`

- [ ] **Step 3: Smoke-check Streamlit import**

Run: `/Users/smx/.pyenv/versions/3.11.8/bin/python3.11 -c "import streamlit_app; print('streamlit-app-ok')"`
Expected: `streamlit-app-ok`
