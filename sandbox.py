import streamlit as st
from streamlit_ace import st_ace
import json
import time
import io
import sys

st.set_page_config(layout="wide")
result_placeholder = st.empty()  # Placeholder for the result
result = {}
st.header("Sandbox")
col1, col2 = st.columns(2)

with col1:
    code = st_ace(
        value="# Write your Python code here",
        language="python",
        theme="monokai",
        key="code_editor",  # Assign a key to maintain state
        height=500,
    )
    with st.spinner("Running code..."):
        try:
            output_buffer = io.StringIO()
            sys.stdout = output_buffer
            exec(code, globals(), {})
            result = output_buffer.getvalue()
        except Exception as e:
            st.error(f"Error: {e}")
            time.sleep(2)

with col2:
    card_markdown = f"""
    <div class="card" style="background-color: #2F3129; height: 500px; padding: 20px; margin: auto; color: white;margin-top:8px">
        <div class="card-body">
            <pre>{result}</pre>
        </div>
    </div>
    """
    st.markdown(card_markdown, unsafe_allow_html=True)
    st.markdown(
    """
    <style>
    .stButton {
        display:flex;
        justify-content: flex-end;
    }
    .stButton > button {
        justify-content: flex-end;
    }
    </style>
    """,
    unsafe_allow_html=True,
    )   
    if st.button("Clear"):
        result = {}
        result_placeholder.empty()  # Clear the result placeholder
