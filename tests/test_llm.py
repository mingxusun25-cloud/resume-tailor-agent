from resumetailor_agent.config import AppConfig
from resumetailor_agent.llm import _merge_constrained_resume_output, enhance_resume_output


def test_enhance_resume_output_returns_original_in_rule_mode():
    config = AppConfig()
    resume_output = {
        "fit_summary": "重点围绕 Python 组织简历内容",
        "project_highlights": ["Agent Daily: Built a Python workflow."],
        "skills_summary": "Python, Agent",
        "self_intro": "候选人具备 Python 相关实践。",
        "matched_requirements": ["Matches keyword: Python"],
    }

    enhanced = enhance_resume_output(config, resume_output, {"keywords": ["Python"]}, [])

    assert enhanced["fit_summary"] == resume_output["fit_summary"]
    assert enhanced["llm_enhanced"] is False


def test_merge_constrained_resume_output_discards_invalid_fields():
    draft = {
        "fit_summary": "rule summary",
        "project_highlights": ["Agent Daily: Built a Python workflow."],
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
    assert merged["self_intro"] == "new intro"


def test_merge_constrained_resume_output_rejects_unsupported_claims():
    draft = {
        "fit_summary": "rule summary",
        "project_highlights": ["Agent Daily: Built a Python workflow."],
        "skills_summary": "Python, Agent",
        "self_intro": "候选人具备 Python 相关实践。",
        "matched_requirements": ["Matches keyword: Python"],
    }
    enhanced = {
        "fit_summary": "Built a Kubernetes platform for large-scale distributed training.",
        "self_intro": "候选人主导了分布式训练平台架构。",
    }

    merged = _merge_constrained_resume_output(
        draft,
        enhanced,
        evidence_lines=["Agent Daily: Built a Python workflow for GitHub reports."],
    )

    assert merged["fit_summary"] == draft["fit_summary"]
    assert merged["self_intro"] == draft["self_intro"]
