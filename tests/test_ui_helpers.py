from resumetailor_agent.ui_helpers import parse_compare_inputs


def test_parse_compare_inputs_converts_labeled_blocks():
    pairs = parse_compare_inputs("AI应用::需要 Python\n---\n演示岗::需要 Streamlit")

    assert pairs == [("AI应用", "需要 Python"), ("演示岗", "需要 Streamlit")]
