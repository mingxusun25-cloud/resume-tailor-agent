from resumetailor_agent.schemas import JobRequirement, MaterialChunk, RunContext


def test_run_context_starts_with_empty_workflow_state():
    context = RunContext(jd_raw="Need Python and Agent workflow experience")

    assert context.jd_raw.startswith("Need Python")
    assert context.query_plan.query_tokens == []
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
