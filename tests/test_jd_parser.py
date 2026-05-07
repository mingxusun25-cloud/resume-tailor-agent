from resumetailor_agent.nodes.jd_parser import parse_job_description


def test_parse_job_description_extracts_keywords_and_must_have():
    jd = "AI应用实习生，要求熟悉 Python、RAG、Agent 工作流，有自动化项目经验。"

    parsed = parse_job_description(jd)

    assert "Python" in parsed.keywords
    assert "RAG" in parsed.keywords
    assert "Agent" in parsed.keywords
    assert any("自动化" in item for item in parsed.must_have)


def test_parse_job_description_extracts_nice_to_have_and_target_level():
    jd = "AI应用实习生，要求熟悉 Python 和 Agent 工作流，有自动化项目经验；加分项：RAG、Streamlit、GitHub 项目经验。"

    parsed = parse_job_description(jd)

    assert parsed.target_level == "intern"
    assert any("RAG" in item for item in parsed.nice_to_have)
    assert "Streamlit" in parsed.keywords
