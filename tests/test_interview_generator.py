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
