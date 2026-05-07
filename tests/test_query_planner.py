from resumetailor_agent.nodes.query_planner import build_query_plan
from resumetailor_agent.schemas import JobRequirement


def test_build_query_plan_expands_keywords_and_tokens():
    requirement = JobRequirement(
        keywords=["Python", "Agent", "自动化"],
        must_have=["要求有自动化项目经验"],
        nice_to_have=["加分项：RAG"],
    )

    plan = build_query_plan(requirement)

    assert "python" in plan.query_tokens
    assert "agent" in plan.query_tokens
    assert "workflow" in plan.expanded_terms
    assert "automation" in plan.expanded_terms
    assert "python" in plan.query_text
