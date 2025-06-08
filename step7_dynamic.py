import pandas as pd
import streamlit as st

# Load worksheet once
_data = pd.read_excel("step7_data.xlsx")


def _build_expr(row: pd.Series) -> str:
    """Return the condition expression to evaluate."""
    expr = row.get("output_condition_all_met", "")
    if isinstance(expr, str):
        expr = expr.strip()
        if expr.startswith("if "):
            expr = expr[3:]
        if expr.endswith(":"):
            expr = expr[:-1]
        return expr.strip()
    return ""


_data["expr"] = _data.apply(_build_expr, axis=1)
for col in ["subitem_met", "requirements_met", "requirements_unmet"]:
    if col in _data.columns:
        _data.drop(columns=col, inplace=True)


def render_step7(step6_items: dict) -> None:
    if "step7_page" not in st.session_state:
        st.session_state.step7_page = 0
    if "step7_results" not in st.session_state:
        st.session_state.step7_results = {}

    step6_selections = st.session_state.step6_selections
    targets = st.session_state.step6_targets
    total_pages = len(targets)
    current_key = targets[st.session_state.step7_page]

    st.markdown("## 제조방법 변경에 따른 필요서류 및 보고유형")
    st.markdown(step6_items[current_key]["title"])

    hits = []
    rows = _data[_data["title_key"] == current_key]
    for _, row in rows.iterrows():
        expr = row["expr"]
        if not expr:
            continue
        if eval(expr, {}, {"step6_selections": step6_selections}):
            st.markdown(row["output_1_text"], unsafe_allow_html=True)
            st.markdown(row["output_2_text"], unsafe_allow_html=True)
            hits.append((row["output_1_tag"], row["output_1_text"], row["output_2_text"]))

    if not hits:
        st.warning(
            "해당 변경사항에 대한 충족조건을 고려하였을 때,\n"
            "「의약품 허가 후 제조방법 변경관리 가이드라인」에서 제시하고 있는\n"
            "범위에 해당하지 않는 것으로 확인됩니다"
        )

    st.session_state.step7_results[current_key] = hits

    col1, col2 = st.columns(2)
    with col1:
        st.button(
            "이전단계로",
            on_click=lambda: st.session_state.__setitem__(
                "step7_page", st.session_state.step7_page - 1
            ),
            disabled=st.session_state.step7_page == 0,
        )
    with col2:
        if st.session_state.step7_page == total_pages - 1:
            st.button(
                "신청양식 확인하기",
                on_click=lambda: st.session_state.__setitem__("step", 8),
            )
        else:
            st.button(
                "다음단계로",
                on_click=lambda: st.session_state.__setitem__(
                    "step7_page", st.session_state.step7_page + 1
                ),
            )
