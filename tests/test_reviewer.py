from resumetailor_agent.config import AppConfig
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


def test_review_resume_output_merges_model_review_findings():
    resume_output = {
        "project_highlights": ["Built a Python Agent workflow."],
        "skills_summary": "Python, Agent",
    }
    evidence_texts = ["Built a Python Agent workflow for GitHub tracking."]
    model_review = {
        "risk_level": "high",
        "issues": ["Model review: missing proof for production deployment."],
        "evidence_gaps": ["No deployment evidence"],
        "mode": "llm_review",
    }

    review = review_resume_output(
        resume_output,
        evidence_texts,
        mode="llm",
        model_review=model_review,
    )

    assert review["risk_level"] == "high"
    assert "Model review: missing proof for production deployment." in review["issues"]
    assert review["review_layers"] == ["rule", "model"]


def test_review_resume_output_returns_disabled_model_payload_without_credentials():
    config = AppConfig()

    review = review_resume_output(
        {"project_highlights": ["Built a Python Agent workflow."]},
        ["Built a Python Agent workflow."],
        mode=config.mode,
        config=config,
    )

    assert review["model_review"]["enabled"] is False
