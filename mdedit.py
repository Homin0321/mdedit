import streamlit as st

st.set_page_config(layout="wide", page_title="Markdown Editor", page_icon="📝")

st.session_state.text = st.session_state.get("text", "")

tab1, tab2 = st.tabs(["Edit", "Preview"])

with tab1:
    st.text_area("Edit Markdown:", key="text", height=800)

with tab2:
    st.markdown(st.session_state.text)
