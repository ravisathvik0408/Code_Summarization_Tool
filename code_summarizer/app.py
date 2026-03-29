import streamlit as st
import time
import ast
from ast_parser.parser import parse_to_ast
from ast_parser.ast_serializer import get_ast_summary_info
from summarizer.model import generate_summary
from data.save_samples import save_sample, load_samples

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Code Summarizer",
    page_icon="🧠",
    layout="wide"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Sora:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Sora', sans-serif;
    }
    code, textarea, .stTextArea textarea {
        font-family: 'JetBrains Mono', monospace !important;
    }
    .title-block {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
    }
    .title-block h1 {
        color: #00e5ff;
        font-size: 2.2rem;
        margin: 0;
    }
    .title-block p {
        color: #b0bec5;
        margin: 0.4rem 0 0 0;
        font-size: 1rem;
    }
    .summary-box {
        background: #1a1a2e;
        border-left: 4px solid #00e5ff;
        padding: 1.2rem 1.5rem;
        border-radius: 10px;
        color: #e0f7fa;
        font-size: 1.1rem;
        margin-top: 1rem;
    }
    .ast-box {
        background: #0d1117;
        border: 1px solid #30363d;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        color: #8b949e;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.85rem;
    }
    .stButton > button {
        background: linear-gradient(90deg, #00b4db, #0083b0);
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #0083b0, #00b4db);
        transform: scale(1.02);
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="title-block">
    <h1>🧠 NLP-Based Code Summarization Tool</h1>
    <p>Paste Python code → Get a natural language summary using CodeT5 Transformer</p>
</div>
""", unsafe_allow_html=True)

# ── Layout ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("### 📥 Input Code")
    code = st.text_area(
        label="Enter Python code here:",
        height=300,
        placeholder="def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)",
        label_visibility="collapsed"
    )

    summarize_btn = st.button("⚡ Generate Summary")

with col2:
    st.markdown("### 📤 Output")

    if summarize_btn:
        if not code.strip():
            st.error("⚠️ Please enter some Python code first.")
        else:
            # AST Validation
            tree = parse_to_ast(code)
            if tree is None:
                st.error("❌ Syntax Error detected in your code. Please fix it and try again.")
            else:
                # AST Info
                info = get_ast_summary_info(tree)
                node_count = len(list(ast.walk(tree)))
                st.markdown("**🌳 AST Structure Info:**")
                st.markdown(f"""
<div class="ast-box">
Functions : {info['functions'] if info['functions'] else 'None'}<br>
Classes   : {info['classes'] if info['classes'] else 'None'}<br>
Imports   : {info['imports'] if info['imports'] else 'None'}<br>
AST Nodes : {node_count}
</div>
""", unsafe_allow_html=True)

                # Generate Summary
                with st.spinner("🤖 Generating summary with CodeT5..."):
                    start_time = time.time()
                    summary = generate_summary(code)
                    end_time = time.time()

                st.markdown("**📝 Generated Summary:**")
                st.markdown(f'<div class="summary-box">💬 {summary}</div>', unsafe_allow_html=True)

                st.write(f"⏱ Execution Time: {end_time - start_time:.2f} seconds")


                st.download_button(
                  label="📥 Download Summary",
                    data=summary,
                    file_name="summary.txt",
                    mime="text/plain"
                )
                 
                 
                # Save
                save_sample(code, summary)
                st.success("✅ Sample saved to data/samples.json")

# ── History Section ───────────────────────────────────────────────────────────
st.markdown("---")
if st.button("🗑 Clear History"):
    with open("data/samples.json", "w") as f:
        f.write("[]")
    st.success("History cleared successfully!")
st.markdown("### 📚 Previous Summaries")

samples = load_samples()
if not samples:
    st.info("No samples saved yet. Generate your first summary above!")
else:
    for i, s in enumerate(reversed(samples[-5:]), 1):
        with st.expander(f"Sample {len(samples) - i + 1} — {s['timestamp']}"):
            st.code(s["code"], language="python")
            st.markdown(f"**Summary:** {s['summary']}")
