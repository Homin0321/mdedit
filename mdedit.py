import streamlit as st

st.set_page_config(layout="wide", page_title="Markdown Editor", page_icon="📝")

if "text" not in st.session_state:
    st.session_state.text = ""

tab1, tab2 = st.tabs(["Edit", "Preview"])

with tab1:
    st.session_state.text = st.text_area("Edit Markdown:", st.session_state.text, height=800)

with tab2:
    st.markdown(st.session_state.text)
