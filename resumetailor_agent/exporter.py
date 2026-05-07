from __future__ import annotations

import json
from pathlib import Path


def export_markdown_report(
    output_dir: Path,
    run_id: str,
    jd_summary: dict[str, object],
    evidence_lines: list[str],
    resume_output: dict[str, object],
    review_output: dict[str, object],
    interview_output: dict[str, object] | None = None,
    gap_output: dict[str, object] | None = None,
    query_plan: dict[str, object] | None = None,
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{run_id}.md"

    project_highlights = resume_output.get("project_highlights", [])
    skills_summary = resume_output.get("skills_summary", "")
    fit_summary = resume_output.get("fit_summary", "")
    self_intro = resume_output.get("self_intro", "")
    matched_requirements = resume_output.get("matched_requirements", [])
    issues = review_output.get("issues", [])
    review_layers = review_output.get("review_layers", ["rule"])
    model_review = review_output.get("model_review", {})
    questions = []
    if interview_output:
        questions = interview_output.get("questions", [])
    matched_keywords = []
    missing_keywords = []
    weak_requirements = []
    suggestions = []
    suggestion_cards = []
    gap_level = "low"
    if gap_output:
        matched_keywords = gap_output.get("matched_keywords", [])
        missing_keywords = gap_output.get("missing_keywords", [])
        weak_requirements = gap_output.get("weak_requirements", [])
        suggestions = gap_output.get("suggestions", [])
        suggestion_cards = gap_output.get("suggestion_cards", [])
        gap_level = gap_output.get("gap_level", "low")
    query_tokens = []
    expanded_terms = []
    if query_plan:
        query_tokens = query_plan.get("query_tokens", [])
        expanded_terms = query_plan.get("expanded_terms", [])

    lines = [
        "# 岗位 JD 定制结果",
        "",
        "## 1. JD 解析摘要",
        f"- 关键词: {', '.join(jd_summary.get('keywords', []))}",
        "",
        "## 1.1 查询计划",
        f"- query_tokens: {', '.join(query_tokens) if query_tokens else '暂无'}",
        f"- expanded_terms: {', '.join(expanded_terms) if expanded_terms else '暂无'}",
        "",
        "## 2. 命中经历证据",
    ]
    lines.extend(f"- {line}" for line in evidence_lines or ["未命中素材"])
    lines.extend(
        [
            "",
            "## 3. 定制化项目描述",
        ]
    )
    lines.extend(f"- {line}" for line in project_highlights or ["暂无项目亮点"])
    lines.extend(
        [
            "",
            "## 4. 技能描述优化建议",
            f"- {skills_summary or '暂无技能摘要'}",
            "",
            "## 5. 自我介绍摘要",
            f"- {self_intro or fit_summary or '暂无适配摘要'}",
            "",
            "## 5.1 匹配依据",
        ]
    )
    lines.extend(f"- {line}" for line in matched_requirements or ["暂无匹配依据"])
    lines.extend(
        [
            "",
            "## 6. 面试高频追问",
        ]
    )
    if questions:
        lines.extend(
            f"- {item.get('question', '')} | 提示: {item.get('hint', '')}"
            for item in questions
            if isinstance(item, dict)
        )
    else:
        lines.append("- 暂无面试追问")

    lines.extend(
        [
            "",
            "## 7. 素材缺口分析",
            f"- 缺口等级: {gap_level}",
            f"- 已覆盖关键词: {', '.join(matched_keywords) if matched_keywords else '暂无'}",
            f"- 缺失关键词: {', '.join(missing_keywords) if missing_keywords else '无明显缺口'}",
            f"- 薄弱要求: {' | '.join(weak_requirements) if weak_requirements else '暂无明显薄弱项'}",
        ]
    )
    if suggestion_cards:
        lines.extend(
            f"- 建议: {item.get('keyword', '')} -> {item.get('action', '')} | 证据提示: {item.get('evidence_hint', '')}"
            for item in suggestion_cards
            if isinstance(item, dict)
        )
    else:
        lines.extend(f"- 建议: {suggestion}" for suggestion in suggestions)

    lines.extend(
        [
            "",
            "## 8. 风险提示与建议",
            f"- 风险等级: {review_output.get('risk_level', 'unknown')}",
            f"- review_layers: {', '.join(review_layers)}",
            f"- model_review_enabled: {model_review.get('enabled', False)}",
        ]
    )
    lines.extend(f"- {issue}" for issue in issues or ["未发现明显风险"])

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def export_run_log(output_dir: Path, run_id: str, payload: dict[str, object]) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{run_id}.json"
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path


def export_comparison_report(output_dir: Path, run_id: str, summary: dict[str, object]) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{run_id}-comparison.md"

    common_keywords = summary.get("common_keywords", [])
    comparison_rows = summary.get("comparison_rows", [])
    lines = [
        "# 多 JD 对比结果",
        "",
        "## 1. 共同关键词",
        f"- {', '.join(common_keywords) if common_keywords else '无明显共同关键词'}",
        "",
        "## 2. 岗位对比明细",
    ]

    for row in comparison_rows:
        if not isinstance(row, dict):
            continue
        lines.extend(
            [
                f"### {row.get('label', '未命名岗位')}",
                f"- 关键词: {', '.join(row.get('keywords', [])) or '暂无'}",
                f"- 差异关键词: {', '.join(row.get('unique_keywords', [])) or '无'}",
                f"- 主命中项目: {row.get('top_project', '暂无')}",
                f"- 缺失关键词: {', '.join(row.get('missing_keywords', [])) or '无'}",
                f"- 风险等级: {row.get('risk_level', 'unknown')}",
                f"- 单岗位报告: {row.get('export_path', '') or '暂无'}",
                "",
            ]
        )

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path


def export_evaluation_report(
    output_dir: Path,
    run_id: str,
    summary: dict[str, object],
    case_rows: list[dict[str, object]],
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{run_id}-evaluation.md"

    lines = [
        "# 结果质量评估",
        "",
        "## 1. 总览",
        f"- Case 数量: {summary.get('case_count', 0)}",
        f"- 平均关键词召回: {summary.get('average_keyword_recall', 0.0)}",
        f"- 平均项目命中: {summary.get('average_project_hit', 0.0)}",
        f"- 平均总分: {summary.get('average_overall_score', 0.0)}",
        "",
        "## 2. Case 明细",
    ]

    for row in case_rows:
        lines.extend(
            [
                f"### {row.get('label', '未命名 case')}",
                f"- 期望关键词: {', '.join(row.get('expected_keywords', [])) or '暂无'}",
                f"- 实际命中关键词: {', '.join(row.get('matched_keywords', [])) or '暂无'}",
                f"- 缺失关键词: {', '.join(row.get('missing_keywords', [])) or '无'}",
                f"- 关键词召回: {row.get('keyword_recall', 0.0)}",
                f"- 项目命中: {row.get('project_hit', 0.0)}",
                f"- 证据存在: {row.get('evidence_presence', 0.0)}",
                f"- 风险等级: {row.get('risk_level', 'unknown')}",
                f"- 综合得分: {row.get('overall_score', 0.0)}",
                f"- 单次报告: {row.get('report_path', '') or '暂无'}",
                "",
            ]
        )

    output_path.write_text("\n".join(lines), encoding="utf-8")
    return output_path
