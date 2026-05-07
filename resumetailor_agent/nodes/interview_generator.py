from __future__ import annotations


def build_interview_output(resume_output: dict[str, object]) -> dict[str, object]:
    questions: list[dict[str, str]] = []
    seen_titles: set[str] = set()
    project_highlights = resume_output.get("project_highlights", [])

    if isinstance(project_highlights, list):
        for highlight in project_highlights[:3]:
            if not isinstance(highlight, str) or ":" not in highlight:
                continue
            title, detail = highlight.split(":", 1)
            cleaned_title = title.strip()
            cleaned_detail = detail.strip()
            if cleaned_title in seen_titles:
                continue
            seen_titles.add(cleaned_title)
            questions.append(
                {
                    "question": f"Can you walk through how {cleaned_title} was implemented?",
                    "hint": cleaned_detail,
                }
            )

    if not questions:
        questions.append(
            {
                "question": "Which experience best matches this JD, and why?",
                "hint": str(resume_output.get("fit_summary", "")),
            }
        )

    return {"questions": questions}
