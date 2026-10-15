
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ==================================================
# PAGE CONFIGURATION
# ==================================================
st.set_page_config(
    page_title="PromptLab | AI Prompt Evaluation",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# SESSION STORAGE
# ==================================================
if "evaluation_history" not in st.session_state:
    st.session_state.evaluation_history = []

# ==================================================
# CUSTOM DESIGN
# ==================================================
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

.hero {
    padding: 30px;
    border-radius: 18px;
    background: linear-gradient(120deg, #172554, #4338ca);
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    color: white;
    font-size: 32px;
}

.hero p {
    color: #e0e7ff;
    font-size: 16px;
}

.team {
    color: #c7d2fe;
    font-size: 14px;
    margin-top: 15px;
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# PROMPT EVALUATION FUNCTION
# ==================================================
def evaluate_prompt(prompt):
    text = prompt.lower()

    checks = {
        "Clear task": len(prompt.split()) >= 5,

        "Role prompting": any(
            word in text
            for word in ["act as", "you are", "your role"]
        ),

        "Context or audience": any(
            word in text
            for word in [
                "beginner", "student", "context", "audience"
            ]
        ),

        "Constraints": any(
            word in text
            for word in [
                "must", "within", "limit", "avoid",
                "only", "under", "maximum"
            ]
        ),

        "Output format": any(
            word in text
            for word in [
                "bullet points", "table", "format",
                "list", "numbered"
            ]
        ),

        "Examples": any(
            word in text
            for word in [
                "example", "examples", "sample", "few-shot"
            ]
        )
    }

    score = round(
        sum(checks.values()) / len(checks) * 10, 2
    )

    suggestions = [
        f"Consider adding: {criterion}"
        for criterion, passed in checks.items()
        if not passed
    ]

    return score, checks, suggestions


# ==================================================
# PROMPT OPTIMIZATION FUNCTION
# ==================================================
def optimize_prompt(prompt):
    prompt = prompt.strip()

    if not prompt:
        return ""

    text = prompt.lower()
    additions = []

    if not any(word in text for word in [
        "act as", "you are", "your role"
    ]):
        additions.append("Act as a knowledgeable teacher")

    if not any(word in text for word in [
        "beginner", "student", "audience"
    ]):
        additions.append("explain it to a beginner")

    if not any(word in text for word in [
        "example", "examples", "sample", "few-shot"
    ]):
        additions.append("include two simple real-world examples")

    if not any(word in text for word in [
        "bullet points", "table", "format", "list"
    ]):
        additions.append("organize the answer into bullet points")

    if not any(word in text for word in [
        "within", "limit", "under", "maximum"
    ]):
        additions.append("keep the answer under 200 words")

    if additions:
        improved = (
            ", ".join(additions).capitalize()
            + ". Task: "
            + prompt.rstrip(".!? ")
            + "."
        )
    else:
        improved = prompt

    return improved


# ==================================================
# HEADER
# ==================================================
st.markdown("""
<div class="hero">
    <h1>🧠 AI Prompt Evaluation & Optimization Framework</h1>
    <p>
        Compare prompt structures, evaluate quality criteria,
        and discover ways to improve your prompts.
    </p>
    <div class="team">
        PROMPT ENGINEERING LAB | MINI PROJECT
        <br><br>
        Developed by: Yatharth and Abhishek
    </div>
</div>
""", unsafe_allow_html=True)

# ==================================================
# SIDEBAR NAVIGATION
# ==================================================
with st.sidebar:
    st.title("🧠 PromptLab")
    st.caption("Prompt Engineering Mini Project")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Prompt Evaluation",
            "About Project"
        ]
    )

    st.divider()
    st.caption("Developed by")
    st.write("👨‍💻 Yatharth")
    st.write("👨‍💻 Abhishek")

    st.divider()
    st.caption("Offline rule-based application")
    st.caption("No API required")

# ==================================================
# DASHBOARD
# ==================================================
if page == "Dashboard":

    st.subheader("Project Dashboard")

    st.write(
        "Welcome to PromptLab, a tool for comparing prompts "
        "and identifying useful prompt-design features."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Evaluation Criteria", "6")
    col2.metric("Prompts per Comparison", "2")
    col3.metric("Score Scale", "0–10")

    st.divider()
    st.subheader("How It Works")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("### ✍️ Enter")
        st.write("Provide two prompts designed for the same task.")

    with c2:
        st.markdown("### 📊 Evaluate")
        st.write("Compare both prompts using six structural checks.")

    with c3:
        st.markdown("### ✨ Optimize")
        st.write("Generate an improved prompt and compare its score.")

    st.divider()
    st.subheader("Recent Evaluation Activity")

    if st.session_state.evaluation_history:
        history_df = pd.DataFrame(
            st.session_state.evaluation_history
        )
        st.dataframe(
            history_df.tail(5).iloc[::-1],
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info(
            "No evaluations yet. Open Prompt Evaluation to begin."
        )

# ==================================================
# PROMPT EVALUATION PAGE
# ==================================================
elif page == "Prompt Evaluation":

    st.subheader("Prompt Comparison Workspace")

    st.write(
        "Enter two prompts intended for the same task. "
        "Evaluate their structure and compare the results."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📝 Prompt A")

        prompt_a = st.text_area(
            "Original prompt",
            value="Explain machine learning.",
            height=160,
            key="prompt_a"
        )

    with col2:
        st.markdown("### ✨ Prompt B")

        prompt_b = st.text_area(
            "Alternative prompt",
            value=(
                "Act as a teacher. Explain machine learning "
                "to a beginner using examples and bullet points. "
                "Keep the answer within 200 words."
            ),
            height=160,
            key="prompt_b"
        )

    if st.button(
        "Evaluate and Compare Prompts",
        type="primary",
        use_container_width=True
    ):

        if not prompt_a.strip() or not prompt_b.strip():
            st.warning("Please enter both prompts.")

        else:
            score_a, checks_a, suggestions_a = evaluate_prompt(prompt_a)
            score_b, checks_b, suggestions_b = evaluate_prompt(prompt_b)

            st.session_state.latest_comparison = {
                "prompt_a": prompt_a,
                "prompt_b": prompt_b,
                "score_a": score_a,
                "score_b": score_b,
                "checks_a": checks_a,
                "checks_b": checks_b,
                "suggestions_a": suggestions_a,
                "suggestions_b": suggestions_b
            }

            st.session_state.evaluation_history.append({
                "Time": datetime.now().strftime("%H:%M:%S"),
                "Prompt A": prompt_a[:80],
                "Prompt B": prompt_b[:80],
                "Score A": score_a,
                "Score B": score_b
            })

    # Display the latest comparison after evaluation
    result = st.session_state.get("latest_comparison")

    if result:
        st.divider()
        st.subheader("Evaluation Results")

        m1, m2, m3 = st.columns(3)

        m1.metric(
            "Prompt A Score",
            f"{result['score_a']}/10"
        )

        m2.metric(
            "Prompt B Score",
            f"{result['score_b']}/10"
        )

        m3.metric(
            "Score Difference",
            f"{abs(result['score_a'] - result['score_b']):.2f}"
        )

        results_df = pd.DataFrame({
            "Criterion": list(result["checks_a"].keys()),
            "Prompt A": [
                "Pass" if value else "Needs improvement"
                for value in result["checks_a"].values()
            ],
            "Prompt B": [
                "Pass" if value else "Needs improvement"
                for value in result["checks_b"].values()
            ]
        })

        st.subheader("Criterion-by-Criterion Comparison")

        st.dataframe(
            results_df,
            hide_index=True,
            use_container_width=True
        )

        st.subheader("Prompt Quality Comparison")

        fig, ax = plt.subplots(figsize=(8, 4))

        bars = ax.bar(
            ["Prompt A", "Prompt B"],
            [result["score_a"], result["score_b"]]
        )

        ax.set_ylim(0, 10)
        ax.set_ylabel("Structural score out of 10")
        ax.set_title("Prompt Quality Comparison")
        ax.bar_label(bars, fmt="%.2f")
        ax.grid(axis="y", alpha=0.2)

        st.pyplot(fig)
        plt.close(fig)

        s1, s2 = st.columns(2)

        with s1:
            st.markdown("### Prompt A Suggestions")

            if result["suggestions_a"]:
                for suggestion in result["suggestions_a"]:
                    st.write("• " + suggestion)
            else:
                st.success("All structural checks passed.")

        with s2:
            st.markdown("### Prompt B Suggestions")

            if result["suggestions_b"]:
                for suggestion in result["suggestions_b"]:
                    st.write("• " + suggestion)
            else:
                st.success("All structural checks passed.")

        if result["score_a"] > result["score_b"]:
            st.info("Prompt A scores higher on the structural rubric.")
        elif result["score_b"] > result["score_a"]:
            st.info("Prompt B scores higher on the structural rubric.")
        else:
            st.info("Both prompts have the same structural score.")

        st.caption(
            "Scores measure predefined structural features only. "
            "They do not establish factual accuracy or actual "
            "AI-generated response quality."
        )

    # --------------------------------------------------
    # AUTOMATIC PROMPT OPTIMIZATION
    # --------------------------------------------------
    st.divider()
    st.subheader("✨ Automatic Prompt Optimization")

    prompt_to_optimize = st.text_area(
        "Enter a prompt to improve",
        value="Explain machine learning.",
        key="optimizer_input"
    )

    if st.button("Optimize Prompt", type="primary"):

        improved_prompt = optimize_prompt(prompt_to_optimize)

        if improved_prompt:
            original_score, _, original_suggestions = (
                evaluate_prompt(prompt_to_optimize)
            )

            improved_score, _, improved_suggestions = (
                evaluate_prompt(improved_prompt)
            )

            st.session_state.latest_optimization = {
                "original": prompt_to_optimize,
                "improved": improved_prompt,
                "original_score": original_score,
                "improved_score": improved_score
            }

    # Keep the latest optimization visible after Streamlit reruns
    optimization = st.session_state.get("latest_optimization")

    if optimization:
        st.success("Optimized prompt generated!")

        c1, c2 = st.columns(2)

        with c1:
            st.markdown("### Original Prompt")

            st.text_area(
                "Original prompt text",
                value=optimization["original"],
                height=180,
                disabled=True,
                key="original_display"
            )

            st.metric(
                "Original Structural Score",
                f"{optimization['original_score']}/10"
            )

        with c2:
            st.markdown("### Optimized Prompt")

            st.text_area(
                "Optimized prompt text",
                value=optimization["improved"],
                height=180,
                disabled=True,
                key="improved_display"
            )

            st.metric(
                "Optimized Structural Score",
                f"{optimization['improved_score']}/10"
            )

        st.markdown("### Copy-Ready Optimized Prompt")

        st.code(optimization["improved"], language=None)

        st.text_input(
            "Select the text below to copy",
            value=optimization["improved"],
            key="copy_ready_prompt"
        )

        st.caption(
            "Click inside the copy-ready box, press Ctrl+A, "
            "then Ctrl+C. This is a manual copy method."
        )

        st.caption(
            "Optimization uses predefined rules, not an AI model. "
            "Review the result before using it."
        )

    # --------------------------------------------------
    # EVALUATION HISTORY
    # --------------------------------------------------
    st.divider()
    st.subheader("📚 Evaluation History")

    if st.session_state.evaluation_history:

        history_df = pd.DataFrame(
            st.session_state.evaluation_history
        )

        st.dataframe(
            history_df,
            hide_index=True,
            use_container_width=True
        )

        if st.button("Clear Evaluation History"):
            st.session_state.evaluation_history = []
            st.rerun()

    else:
        st.info("Your evaluation history will appear here.")

# ==================================================
# ABOUT PROJECT
# ==================================================
elif page == "About Project":

    st.subheader("About the Project")

    st.markdown("""
### Problem Statement

Writing effective prompts is important when working with
large language models. Comparing prompt structures manually
can be inconsistent.

This project provides a rule-based framework for inspecting
and comparing common prompt-design features.

### Objectives

- Compare two prompts intended for the same task.
- Evaluate six predefined prompt-structure criteria.
- Calculate and visualize structural scores.
- Identify missing prompt components.
- Generate an improved prompt using predefined rules.
- Maintain a session-based evaluation history.

### Prompt Engineering Concepts

- Role prompting
- Context and audience prompting
- Constraint prompting
- Structured output
- Few-shot prompting
- Prompt optimization

### Technologies Used

- Python
- Streamlit
- Pandas
- Matplotlib

### Team Members

- Yatharth
- Abhishek

### Limitations

The evaluation and optimization are rule-based.
The application does not call an AI model, verify factual
accuracy, or measure the semantic quality of generated answers.
History is stored in the current Streamlit session and is
not permanent database storage.
""")

# ==================================================
# FOOTER
# ==================================================
st.divider()

st.caption(
    "PromptLab | AI Prompt Evaluation & Optimization Framework"
)

st.caption(
    "Prompt Engineering Lab Mini Project | Yatharth and Abhishek"
)
