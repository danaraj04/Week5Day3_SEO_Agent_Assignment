import asyncio

import streamlit as st

from seo_workflow import run_seo_workflow


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="AI SEO Content Generator",
    page_icon="🚀",
    layout="wide",
)


# ==========================================
# TITLE
# ==========================================

st.title("🚀 AI Multi-Agent SEO Content Generator")

st.write(
    """
    Enter a topic and let four AI agents work together:

    **Research → Write → SEO Audit → Final Review**
    """
)


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.header("⚙️ SEO Settings")

    word_count = st.selectbox(
        "Target Article Length",
        [
            "Short - 800 words",
            "Medium - 1500 words",
            "Long - 2500 words",
            "Very Long - 4000 words",
        ],
    )

    tone = st.selectbox(
        "Content Tone",
        [
            "Professional",
            "Conversational",
            "Educational",
            "Technical",
            "Friendly",
        ],
    )

    st.markdown("---")

    st.info(
        """
        Four agents are used:

        1. 🔎 SEO Researcher
        2. ✍️ Content Writer
        3. 📊 SEO Checker
        4. ✅ Final Reviewer
        """
    )


# ==========================================
# TOPIC INPUT
# ==========================================

topic = st.text_area(
    "Enter your topic",
    placeholder="Example: Best AI tools for students in 2026",
    height=100,
)


# ==========================================
# GENERATE BUTTON
# ==========================================

generate = st.button(
    "🚀 Generate SEO Content",
    type="primary",
    use_container_width=True,
)


# ==========================================
# RUN WORKFLOW
# ==========================================

if generate:

    if not topic.strip():

        st.warning(
            "Please enter a topic first."
        )

        st.stop()


    enhanced_topic = f"""
        Topic:

        {topic}

        Target article length:

        {word_count}

        Content tone:

        {tone}
        """


    # ======================================
    # PROGRESS
    # ======================================

    progress = st.progress(0)

    status = st.empty()


    try:

        status.info(
            "🔎 Agent 1: Researching topic and SEO trends..."
        )

        progress.progress(20)


        results = asyncio.run(
            run_seo_workflow(enhanced_topic)
        )


        progress.progress(100)

        status.success(
            "✅ All four agents completed successfully!"
        )


        # ======================================
        # RESULTS
        # ======================================

        st.markdown("---")

        st.header("📊 SEO Workflow Results")


        # ======================================
        # AGENT 1
        # ======================================

        with st.expander(
            "🔎 Agent 1 — SEO Research",
            expanded=False,
        ):

            st.markdown(
                results["research"]
            )


        # ======================================
        # AGENT 2
        # ======================================

        with st.expander(
            "✍️ Agent 2 — Content Draft",
            expanded=False,
        ):

            st.markdown(
                results["draft"]
            )


        # ======================================
        # AGENT 3
        # ======================================

        with st.expander(
            "📊 Agent 3 — SEO Audit",
            expanded=False,
        ):

            st.markdown(
                results["seo_audit"]
            )


        # ======================================
        # AGENT 4
        # ======================================

        st.header(
            "✅ Agent 4 — Final SEO Content"
        )

        st.markdown(
            results["final_content"]
        )


        # ======================================
        # DOWNLOAD
        # ======================================

        st.download_button(
            label="⬇️ Download Final Content",
            data=results["final_content"],
            file_name="final_seo_article.md",
            mime="text/markdown",
        )


    except Exception as e:

        st.error(
            f"Workflow failed: {str(e)}"
        )

        st.exception(e)