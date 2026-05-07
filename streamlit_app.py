from __future__ import annotations

from pathlib import Path

import streamlit as st

from resumetailor_agent.config import AppConfig
from resumetailor_agent.ui_helpers import parse_compare_inputs
from resumetailor_agent.workflow import run_resume_tailor, run_resume_tailor_compare


st.set_page_config(page_title="ResumeTailor Agent", layout="wide")
st.title("ResumeTailor Agent")
st.caption("面向岗位 JD 的简历定制系统 V1")

default_materials = Path("sample_materials")
default_output = Path("outputs")

jd_text = st.text_area(
    "岗位 JD",
    value="AI应用实习生，要求 Python、Agent、自动化项目经验。",
    height=180,
)
app_mode = st.radio("运行模式", options=["单 JD", "多 JD 对比"], horizontal=True)
compare_inputs = st.text_area(
    "多 JD 输入",
    value="AI应用::AI应用实习生，要求 Python、Agent、自动化项目经验。\n---\n演示岗::AI应用实习生，要求 Streamlit、Python 项目经验。",
    height=180,
)
materials_path = st.text_input("素材目录", value=str(default_materials))
output_path = st.text_input("输出目录", value=str(default_output))
run_id = st.text_input("运行 ID", value="streamlit-run")
api_key = st.text_input("OpenAI API Key（可选）", value="", type="password")
base_url = st.text_input("OpenAI Base URL（可选）", value="")
model_name = st.text_input("OpenAI Model（可选）", value="")

if st.button("开始生成"):
    config = AppConfig(
        openai_api_key=api_key,
        openai_base_url=base_url or "https://api.openai.com/v1",
        openai_model=model_name,
    )
    if app_mode == "多 JD 对比":
        jd_inputs = parse_compare_inputs(compare_inputs)
        comparison = run_resume_tailor_compare(
            jd_inputs=jd_inputs,
            materials_dir=Path(materials_path),
            output_dir=Path(output_path),
            run_id=run_id,
            config=config,
        )

        st.subheader("多 JD 对比结果")
        st.write({"common_keywords": comparison.summary.get("common_keywords", [])})
        st.dataframe(comparison.summary.get("comparison_rows", []), use_container_width=True)
        compare_tabs = st.tabs(
            [item.jd_parsed.job_title or f"JD {index}" for index, item in enumerate(comparison.runs, start=1)]
        )
        for tab, item, row in zip(compare_tabs, comparison.runs, comparison.summary.get("comparison_rows", [])):
            with tab:
                st.subheader("JD 解析")
                st.json(item.jd_parsed.model_dump())
                st.subheader("对比摘要")
                st.write(
                    {
                        "common_keywords": comparison.summary.get("common_keywords", []),
                        "unique_keywords": row.get("unique_keywords", []),
                        "top_project": row.get("top_project", ""),
                        "missing_keywords": row.get("missing_keywords", []),
                        "risk_level": row.get("risk_level", "unknown"),
                    }
                )
                st.subheader("查询计划")
                st.json(item.query_plan.model_dump())
                st.subheader("项目亮点")
                st.write(item.resume_output.get("project_highlights", []))
                st.subheader("缺口建议")
                st.json(item.gap_output.get("suggestion_cards", item.gap_output))
                st.subheader("风险复核")
                st.json(item.review_output)
        st.write(f"对比 Markdown 输出: `{comparison.export_path}`")
        st.stop()

    result = run_resume_tailor(
        jd_text=jd_text,
        materials_dir=Path(materials_path),
        output_dir=Path(output_path),
        run_id=run_id,
        config=config,
    )

    left, right = st.columns(2)
    with left:
        st.subheader("JD 解析")
        st.json(result.jd_parsed.model_dump())
        st.caption(f"运行模式: {result.review_output.get('mode', 'rule')}")
        st.caption(
            f"生成约束: {result.resume_output.get('constraint_mode', 'rule_only')} | "
            f"LLM 增强: {result.resume_output.get('llm_enhanced', False)}"
        )
        st.subheader("查询计划")
        st.json(result.query_plan.model_dump())
        st.subheader("检索概览")
        metric_left, metric_right = st.columns(2)
        metric_left.metric("素材段落数", len(result.retrieved_chunks))
        metric_right.metric("命中证据数", len(result.ranked_evidence))
        st.subheader("命中证据")
        for item in result.ranked_evidence:
            st.write(
                {
                    "title": item.chunk.title if item.chunk else item.chunk_id,
                    "score": item.score,
                    "reason": item.reason,
                    "excerpt": item.chunk.raw_text if item.chunk else "",
                }
            )
    with right:
        st.subheader("简历输出")
        st.json(result.resume_output)
        st.subheader("匹配依据")
        st.write(result.resume_output.get("matched_requirements", []))
        st.subheader("面试追问")
        st.json(result.interview_output)
        st.subheader("素材缺口")
        st.json(result.gap_output)
        suggestion_cards = result.gap_output.get("suggestion_cards", [])
        if suggestion_cards:
            st.subheader("补强建议卡")
            st.write(suggestion_cards)
        st.subheader("风险检查")
        st.json(result.review_output)
        model_review = result.review_output.get("model_review", {})
        if model_review:
            st.subheader("模型复核")
            st.json(model_review)
        st.write(f"Markdown 输出: `{result.export_path}`")
