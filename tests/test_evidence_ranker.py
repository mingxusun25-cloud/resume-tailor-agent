from resumetailor_agent.nodes.evidence_ranker import rank_evidence_items
from resumetailor_agent.schemas import EvidenceItem, JobRequirement, MaterialChunk


def test_rank_evidence_items_prefers_diverse_titles_over_repetition():
    requirement = JobRequirement(keywords=["Python", "Agent", "Streamlit"])
    repeated_a_1 = EvidenceItem(
        chunk_id="a-1",
        score=8.0,
        reason="Matches keyword: Python",
        chunk=MaterialChunk(
            id="a-1",
            title="GitHub Agent Daily",
            type="project",
            source_file="a.md",
            raw_text="Built a Python Agent automation workflow.",
        ),
    )
    repeated_a_2 = EvidenceItem(
        chunk_id="a-2",
        score=7.8,
        reason="Matches keyword: Agent",
        chunk=MaterialChunk(
            id="a-2",
            title="GitHub Agent Daily",
            type="project",
            source_file="a.md",
            raw_text="Implemented markdown export and evidence organization.",
        ),
    )
    diverse_b = EvidenceItem(
        chunk_id="b-1",
        score=7.1,
        reason="Matches keyword: Streamlit",
        chunk=MaterialChunk(
            id="b-1",
            title="ResumeTailor Agent",
            type="project",
            source_file="b.md",
            raw_text="Used Streamlit to expose matched evidence.",
        ),
    )

    ranked = rank_evidence_items(requirement, [repeated_a_1, repeated_a_2, diverse_b], top_k=2)

    assert len(ranked) == 2
    assert {item.chunk.title for item in ranked if item.chunk} == {
        "GitHub Agent Daily",
        "ResumeTailor Agent",
    }
