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
    evidence = [
        EvidenceItem(
            chunk_id="1",
            score=3.0,
            reason="Matches Python and Agent keywords",
            chunk=chunk,
        )
    ]

    output = build_resume_output(requirement, evidence)

    assert "Agent Daily" in output["project_highlights"][0]
    assert "Python" in output["skills_summary"]


def test_build_resume_output_groups_multiple_chunks_from_same_title():
    requirement = JobRequirement(keywords=["Python", "Agent"])
    chunk_one = MaterialChunk(
        id="1",
        title="ResumeTailor Agent",
        type="project",
        source_file="a.md",
        raw_text="Built a local Python workflow for JD parsing.",
        tags=["Python"],
    )
    chunk_two = MaterialChunk(
        id="2",
        title="ResumeTailor Agent",
        type="project",
        source_file="a.md",
        raw_text="Used Streamlit to expose matched evidence and review results.",
        tags=["Streamlit"],
    )
    evidence = [
        EvidenceItem(chunk_id="1", score=3.0, reason="Matches keyword: Python", chunk=chunk_one),
        EvidenceItem(chunk_id="2", score=2.5, reason="Matches keyword: Agent", chunk=chunk_two),
    ]

    output = build_resume_output(requirement, evidence)

    assert len(output["project_highlights"]) == 1
    assert "JD parsing" in output["project_highlights"][0]
    assert "Streamlit" in output["project_highlights"][0]
