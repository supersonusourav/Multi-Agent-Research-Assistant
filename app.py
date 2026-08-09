import os
import re
import streamlit as st
from workflow import run_workflow
from utils.exporter import generate_docx, generate_pdf


def sanitize_filename(query: str) -> str:
    """Converts a user query into a clean filename."""
    clean = re.sub(r'[^\w\s-]', '', query).strip()
    return re.sub(r'[-\s]+', '_', clean)


# ===================================================
# Page Configuration
# ===================================================
st.set_page_config(
    page_title="Multi-Agent Research Assistant",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ===================================================
# Custom Modern Gradient Theme CSS
# ===================================================
st.markdown(
    """
    <style>
    /* Theme Variables */
    :root {
        --gradient-primary: linear-gradient(135deg, #FF512F 0%, #DD2476 100%);
        --gradient-secondary: linear-gradient(135deg, #FF8008 0%, #FFC837 100%);
        --gradient-card: linear-gradient(145deg, rgba(255, 81, 47, 0.05) 0%, rgba(221, 36, 118, 0.05) 100%);
        --card-border: rgba(255, 81, 47, 0.2);
        --text-color: #2D3748;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 4rem;
        max-width: 1200px;
    }

    /* Title Gradient Styling */
    .gradient-title {
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 900;
        letter-spacing: -0.5px;
        margin-bottom: 0.3rem;
    }
    .gradient-sub-title {
        color: #718096;
        font-size: 1.15rem;
        font-weight: 400;
        margin-bottom: 2rem;
    }

    /* Gradient Buttons */
    div.stButton > button:first-child {
        background: var(--gradient-primary) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 0.75rem 1.5rem !important;
        box-shadow: 0 4px 15px rgba(255, 81, 47, 0.3) !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(255, 81, 47, 0.45) !important;
    }

    /* Stat Card Component */
    .stat-card {
        background: var(--gradient-card);
        border: 1px solid var(--card-border);
        border-radius: 14px;
        padding: 1.25rem 1rem;
        text-align: center;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease;
    }
    .stat-card:hover {
        transform: translateY(-3px);
    }
    .stat-value {
        background: var(--gradient-primary);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.2rem;
        font-weight: 800;
    }
    .stat-label {
        color: #4A5568;
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 0.2rem;
    }

    /* Custom Badges */
    .status-approved {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-block;
        box-shadow: 0 3px 10px rgba(56, 239, 125, 0.3);
    }
    .status-warning {
        background: linear-gradient(135deg, #FF8008 0%, #FFC837 100%);
        color: white;
        padding: 0.5rem 1.2rem;
        border-radius: 30px;
        font-weight: 700;
        font-size: 0.9rem;
        display: inline-block;
        box-shadow: 0 3px 10px rgba(255, 128, 8, 0.3);
    }

    /* Subheader Styling */
    h2, h3 {
        color: #1A202C !important;
        font-weight: 800 !important;
    }

    /* Download Button Glow */
    div.stDownloadButton > button {
        background: var(--gradient-secondary) !important;
        color: white !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(255, 128, 8, 0.25) !important;
    }
    div.stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(255, 128, 8, 0.4) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ===================================================
# Header Section
# ===================================================
st.markdown('<div class="gradient-title">🔍 Multi-Agent Research Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="gradient-sub-title">Autonomous multi-agent synthesis, live web retrieval, and custom paper export engine.</div>',
    unsafe_allow_html=True,
)

# Search Input
query = st.text_input(
    "Research Query",
    placeholder="e.g. Advancements in AI and their societal impact",
    label_visibility="collapsed",
)

col_btn, _ = st.columns([1, 2.5])
with col_btn:
    submit_btn = st.button("✨ Launch Research Workflow", use_container_width=True)

if submit_btn:
    if not query.strip():
        st.warning("Please enter a research topic or query.")
        st.stop()

    with st.spinner("Executing Multi-Agent Graph Workflow..."):
        state = run_workflow(query)
        st.session_state["state"] = state
        st.session_state["query"] = query

# Display Output View
if "state" in st.session_state:
    state = st.session_state["state"]
    current_query = st.session_state.get("query", "Research_Report")

    # ===================================================
    # Key Performance Metrics
    # ===================================================
    st.divider()
    stats = state.get("statistics", {})

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            f'<div class="stat-card"><div class="stat-value">{stats.get("questions", 0)}</div><div class="stat-label">Sub-Queries</div></div>',
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            f'<div class="stat-card"><div class="stat-value">{stats.get("sources", 0)}</div><div class="stat-label">Sources Extracted</div></div>',
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            f'<div class="stat-card"><div class="stat-value">{stats.get("unique_domains", 0)}</div><div class="stat-label">Unique Domains</div></div>',
            unsafe_allow_html=True,
        )
    with c4:
        exec_time = stats.get("execution_time", 0)
        time_str = f"{exec_time:.1f}s" if isinstance(exec_time, (int, float)) else str(exec_time)
        st.markdown(
            f'<div class="stat-card"><div class="stat-value">{time_str}</div><div class="stat-label">Execution Time</div></div>',
            unsafe_allow_html=True,
        )

    # ===================================================
    # Research Plan Agenda
    # ===================================================
    st.divider()
    st.subheader("📌 Research Agenda")

    sub_questions = [q.strip() for q in state.get("sub_questions", "").split("\n") if q.strip()]
    if sub_questions:
        plan_cols = st.columns(min(len(sub_questions), 5))
        for idx, q in enumerate(sub_questions):
            with plan_cols[idx % len(plan_cols)]:
                st.info(f"**{idx+1}.** {q}")

    # ===================================================
    # Report Output & Auto-Exports
    # ===================================================
    st.divider()
    st.subheader("📝 Synthesized Research Report")

    report_text = state.get("report") or state.get("draft", "")

    if report_text:
        # Generate document byte streams for downloading
        docx_bytes, docx_filename = generate_docx(report_text, search_query=current_query)
        pdf_bytes, pdf_filename = generate_pdf(report_text, search_query=current_query)

        d_col1, d_col2 = st.columns(2)
        with d_col1:
            st.download_button(
                label="📄 Download Word (.docx)",
                data=docx_bytes,
                file_name=docx_filename if isinstance(docx_filename, str) else f"{sanitize_filename(current_query)}.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True,
            )
        with d_col2:
            st.download_button(
                label="📥 Download PDF (.pdf)",
                data=pdf_bytes,
                file_name=pdf_filename if isinstance(pdf_filename, str) else f"{sanitize_filename(current_query)}.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        st.markdown(report_text)

    # ===================================================
    # Source Context & Web Data
    # ===================================================
    st.divider()
    st.subheader("🌐 Retrieved Sources")

    if not state.get("research"):
        st.warning("No search results were retrieved.")
    else:
        for item in state["research"]:
            with st.expander(f"🔍 Query: {item.get('question', 'Query Details')}"):
                if not item.get("sources"):
                    st.write("No sources captured for this sub-query.")
                    continue

                for idx, source in enumerate(item["sources"], start=1):
                    st.markdown(f"**[{idx}] {source.get('title', 'Untitled')}**")
                    st.caption(f"URL: {source.get('url', 'N/A')}")
                    st.write(source.get("content", ""))
                    st.markdown("---")

    # ===================================================
    # References List
    # ===================================================
    st.divider()
    st.subheader("📚 Verified Citations")

    citations = state.get("citations", [])
    if citations:
        for i, citation in enumerate(citations, start=1):
            st.markdown(f"**[{i}] {citation.get('title')}**")
            st.caption(citation.get("url"))
    else:
        st.info("No direct citations captured.")

    # ===================================================
    # Critic Review & Logs
    # ===================================================
    st.divider()
    c_col1, c_col2 = st.columns([2, 1])

    with c_col1:
        st.subheader("🔍 Critic Assessment")
        review_text = state.get("critic_review") or state.get("review", "")
        st.write(review_text)

        if state.get("approved"):
            st.markdown('<div class="status-approved">✅ Report Approved</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="status-warning">⚠️ Needs Refinement</div>', unsafe_allow_html=True)

    with c_col2:
        st.subheader("📜 Execution Log")
        log_path = os.path.join("logs", "workflow.log")
        if os.path.exists(log_path):
            try:
                with open(log_path, "r", encoding="utf-8") as f:
                    logs = f.readlines()
                st.text_area("Log Output", "".join(logs[-30:]), height=180, label_visibility="collapsed")
            except Exception:
                st.caption("Unable to read local log file.")
        else:
            st.caption("No active log file found.")