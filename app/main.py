import os
import sys
import tempfile
import streamlit as st

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.agent.agent_builder import create_agent_from_pdf

# Page config
st.set_page_config(page_title="📚 Multi-Source Agent Q&A", layout="wide")
st.title("📚 Multi-Source Agent Assistant")

st.markdown(
    """
    Upload a PDF file and ask any question.
    The AI agent will decide whether to use your file (📄), Arxiv (🧠), or Wikipedia (🌐).
    """
)

# File upload section
uploaded_file = st.file_uploader(
    "📁 Upload a single PDF file", type=["pdf"], accept_multiple_files=False
)

if uploaded_file and st.button("📖 Read Document"):
    # Save to temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    try:
        with st.spinner("⚙️ Setting up your agent..."):
            st.session_state.agent_executor = create_agent_from_pdf(pdf_path)
        st.success("✅ Agent is ready! Ask your question below.")
    except Exception as e:
        st.error(f"❌ Failed to load agent: {e}")

# Question input
question = st.text_input("💬 Ask your question")

if question and "agent_executor" in st.session_state:
    with st.spinner("🤖 Thinking..."):
        try:
            response = st.session_state.agent_executor.invoke({"input": question})

            # Show answer
            st.markdown("### ✅ Answer:")
            st.markdown(response["output"])

            # Show tools used
            intermediate_steps = response.get("intermediate_steps", [])
            if intermediate_steps:
                st.markdown("### 🛠 Tools Used:")
                emoji_map = {
                    "pdf_search": "📄",
                    "arxiv_search": "🧠",
                    "wikipedia_search": "🌐"
                }
                for step in intermediate_steps:
                    tool_name = step[0].tool
                    tool_input = step[0].tool_input
                    emoji = emoji_map.get(tool_name, "🛠")
                    st.markdown(f"- {emoji} **{tool_name}** → `{tool_input}`")

        except Exception as e:
            st.error(f"❌ Something went wrong: {e}")

elif question and "agent_executor" not in st.session_state:
    st.warning("⚠️ Please upload and read a PDF first.")
