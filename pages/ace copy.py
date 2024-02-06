import streamlit as st
from streamlit_ace import st_ace

st.set_page_config(layout="wide")
st.title("Code Editor on Streamlit")

first,second = st.columns(2)
result = {}

with first:
    st.markdown("## Input")
    code = st_ace(language = 'python',
    theme = 'pastel_on_dark',
    height=500) 
    result = {}  # Clear old result
    exec(code, {}, result) 

with second:
    st.markdown("## Output")
    #st.markdown("``` python\n"+code+"```")
    st_ace(value = result,
    language = 'python',
    theme = 'pastel_on_dark',
    height=500,
    readonly  = True)