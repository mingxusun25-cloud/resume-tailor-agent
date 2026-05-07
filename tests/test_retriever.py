from resumetailor_agent.config import AppConfig
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


def test_retrieve_relevant_chunks_returns_explanatory_reason_text():
    requirement = JobRequirement(
        keywords=["Python", "Agent", "RAG"],
        must_have=["自动化项目经验", "GitHub 项目经验"],
    )
    chunks = [
        MaterialChunk(
            id="1",
            title="ResumeTailor Workflow",
            type="project",
            source_file="a.md",
            raw_text="Built a Python Agent workflow with GitHub project tracking and retrieval-based resume customization.",
            tags=["Python", "Agent"],
        )
    ]

    results = retrieve_relevant_chunks(requirement, chunks, top_k=1)

    assert "Python" in results[0].reason
    assert "Agent" in results[0].reason


def test_retrieve_relevant_chunks_reports_vector_signal():
    requirement = JobRequirement(keywords=["Python", "Agent"])
    chunks = [
        MaterialChunk(
            id="1",
            title="Agent Daily",
            type="project",
            source_file="a.md",
            raw_text="Built a Python Agent automation workflow for GitHub trending reports.",
            tags=["Python", "Agent", "automation"],
        )
    ]

    results = retrieve_relevant_chunks(requirement, chunks, top_k=1, config=AppConfig())

    assert results[0].chunk_id == "1"
    assert "Vector score" in results[0].reason
