from pathlib import Path

from resumetailor_agent.exporter import export_comparison_report, export_markdown_report


def test_export_markdown_report_creates_readable_file(tmp_path: Path):
    output_path = export_markdown_report(
        tmp_path,
        "test-run",
        {"keywords": ["Python", "Agent"]},
        ["Agent Daily: matched Python and Agent"],
        {"project_highlights": ["Built an Agent workflow"], "skills_summary": "Python, Agent"},
        {"risk_level": "low", "issues": []},
    )

    content = output_path.read_text(encoding="utf-8")

    assert output_path.exists()
    assert "# 岗位 JD 定制结果" in content
    assert "Built an Agent workflow" in content


def test_export_markdown_report_includes_interview_questions(tmp_path: Path):
    output_path = export_markdown_report(
        tmp_path,
        "test-run",
        {"keywords": ["Python", "Agent"]},
        ["Agent Daily: matched Python and Agent"],
        {"project_highlights": ["Built an Agent workflow"], "skills_summary": "Python, Agent"},
        {"risk_level": "low", "issues": []},
        {"questions": [{"question": "How did Agent Daily use Python?", "hint": "Explain retrieval and export flow."}]},
    )

    content = output_path.read_text(encoding="utf-8")

    assert "## 6. 面试高频追问" in content
    assert "How did Agent Daily use Python?" in content


def test_export_markdown_report_includes_gap_analysis(tmp_path: Path):
    output_path = export_markdown_report(
        tmp_path,
        "gap-run",
        {"keywords": ["Python", "Agent", "RAG"]},
        ["Agent Daily: matched Python and Agent"],
        {"project_highlights": ["Built an Agent workflow"], "skills_summary": "Python, Agent"},
        {"risk_level": "low", "issues": []},
        {"questions": [{"question": "How did Agent Daily use Python?", "hint": "Explain retrieval flow."}]},
        {"matched_keywords": ["Python", "Agent"], "missing_keywords": ["RAG"], "gap_level": "medium"},
    )

    content = output_path.read_text(encoding="utf-8")

    assert "## 7. 素材缺口分析" in content
    assert "缺失关键词: RAG" in content
    assert "缺口等级: medium" in content


def test_export_markdown_report_includes_structured_gap_suggestions(tmp_path: Path):
    output_path = export_markdown_report(
        tmp_path,
        "gap-run",
        {"keywords": ["Python", "RAG"]},
        ["Agent Daily: matched Python"],
        {"project_highlights": ["Built an Agent workflow"], "skills_summary": "Python, Agent"},
        {"risk_level": "low", "issues": []},
        {"questions": []},
        {
            "matched_keywords": ["Python"],
            "missing_keywords": ["RAG"],
            "gap_level": "medium",
            "suggestion_cards": [
                {
                    "keyword": "RAG",
                    "action": "补一段检索增强或知识库问答经历",
                    "evidence_hint": "写清召回、排序、输出链路",
                }
            ],
        },
    )

    content = output_path.read_text(encoding="utf-8")

    assert "补一段检索增强或知识库问答经历" in content
    assert "写清召回、排序、输出链路" in content


def test_export_markdown_report_includes_review_layers_and_query_plan(tmp_path: Path):
    output_path = export_markdown_report(
        tmp_path,
        "review-run",
        {"keywords": ["Python", "Agent"]},
        ["Agent Daily: Matches keyword: Python"],
        {
            "fit_summary": "重点围绕 Python, Agent 组织简历内容",
            "project_highlights": ["Agent Daily: Built a Python workflow."],
            "skills_summary": "Python, Agent",
            "self_intro": "候选人具备 Python, Agent 相关实践。",
            "matched_requirements": ["Matches keyword: Python"],
        },
        {
            "risk_level": "medium",
            "issues": ["Potentially unbacked claim"],
            "review_layers": ["rule", "model"],
            "model_review": {"enabled": True, "risk_level": "medium", "issues": ["Potentially unbacked claim"]},
        },
        gap_output={"matched_keywords": ["Python"], "missing_keywords": ["Agent"], "gap_level": "medium"},
        query_plan={"query_tokens": ["python", "agent"], "expanded_terms": ["python", "agent", "智能体"]},
    )

    content = output_path.read_text(encoding="utf-8")

    assert "查询计划" in content
    assert "review_layers: rule, model" in content


def test_export_comparison_report_summarizes_multiple_jds(tmp_path: Path):
    output_path = export_comparison_report(
        output_dir=tmp_path,
        run_id="compare-run",
        summary={
            "common_keywords": ["Python"],
            "comparison_rows": [
                {
                    "label": "AI应用",
                    "keywords": ["Python", "Agent"],
                    "top_project": "Agent Daily",
                    "missing_keywords": [],
                    "risk_level": "low",
                    "export_path": "outputs/ai.md",
                },
                {
                    "label": "演示岗",
                    "keywords": ["Python", "Streamlit"],
                    "top_project": "ResumeTailor Agent",
                    "missing_keywords": ["Streamlit"],
                    "risk_level": "medium",
                    "export_path": "outputs/demo.md",
                },
            ],
        },
    )

    content = output_path.read_text(encoding="utf-8")

    assert "## 1. 共同关键词" in content
    assert "Python" in content
    assert "演示岗" in content
    assert "缺失关键词: Streamlit" in content
