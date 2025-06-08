# Step 7 Hard-Coded Logic – Integration Guide

> **Scope**  
> This README describes how to run the fully integrated **Steps 1–7** Streamlit app.
> All identifiers, column names, and Korean UI strings **must remain exactly as written**  
> to ensure a 1-to-1 mapping with `step7_data.xlsx`.

---

## 1. Repository Structure

    / (project root)
    ├─ step1_to_7_full.py   # Steps 1 – 7 combined in one script
    ├─ step7_data.xlsx      # worksheet containing evaluation rules & texts
    └─ README.md            # (this file)

---

## 2. Activation Sequence

1. Run `streamlit run step1_to_7_full.py`.
2. Steps 1–7 are all contained in this single script. After Step 6 finishes, `st.session_state.step` becomes `7`.
3. The Step 7 logic runs automatically with no separate import.
4. Final-page button **"신청양식 확인하기"** sets `st.session_state.step = 8`, handing control to Step 8

---

## 3. Required Objects

| Name | Type | Origin | Purpose |
|------|------|--------|---------|
| `step6_targets`      | list[str] | Step 6 | ordered `title_key` list (user choices) |
| `step6_selections`   | dict      | Step 6 | key → `"변경 있음" / "충족" / "미충족"` |
| `step6_items`        | dict      | Step 6 | `title_key` → `{ "title": str }` |
| `step7_page`         | int       | Step 7 | current page index (0-based) |
| `step7_results`      | dict      | Step 7 | `{ title_key: [(output_1_tag, output_1_text, output_2_text), …] }` |

---

## 4. Per-Page UI Flow

| Element | Data / Fixed Text |
|---------|-------------------|
| Header   | `## 제조방법 변경에 따른 필요서류 및 보고유형` |
| Subtitle | `step6_items[current_key]["title"]` |
| Row output | every row where `output_condition_all_met` evaluates **True** → show `output_1_text` + `output_2_text` (HTML) |
| Warning   | shown **only** if no rows hit → `"해당 변경사항에 대한 … 확인됩니다"` |
| Buttons   | `"이전단계로"` (−1) · `"다음단계로"` (+1) · `"신청양식 확인하기"` (+1, final page only) |
@@ -54,25 +54,36 @@
## 5. Data-Integrity Rules

* **Do NOT** invent new column names, session keys, or button labels  
* Keep every Korean string verbatim – no translation or trimming  
* Preserve line-breaks, bullets, and HTML tags inside Excel cells

---

## 6. Step 8 Dependency

`step7_results` is the **sole** data source consumed by Step 8 to build the final
summary and pre-fill the submission form.  
Do not alter its structure.

---

## 7. Quick Setup Checklist

- [ ] Ensure `step7_data.xlsx` is present in the same folder
- [ ] Run `streamlit run step1_to_7_full.py`
- [ ] Step 7 executes automatically whenever `st.session_state.step == 7`

---

## 8. Running the App Locally

Install the dependencies and start Streamlit:

```bash
pip install -r requirements.txt
streamlit run step1_to_7_full.py
```

Step 7 appears automatically whenever `st.session_state.step` becomes `7`.
