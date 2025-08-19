import streamlit as st
import re
import os

st.set_page_config(layout="wide")

with st.sidebar:
    st.title("Markdown Viewer")
    uploaded_md_file = st.file_uploader(
        "Open Markdown file",
        type=["md"]
    )
    image_server_url = st.text_input(
        "Image Server URL",
        "http://127.0.0.1:8080/"
    )

if uploaded_md_file:
    markdown_content = uploaded_md_file.getvalue().decode("utf-8")

    def replace_image_path(match):
        alt_text = match.group(1)
        original_path = match.group(2)
        image_filename = os.path.basename(original_path)
        base_url = image_server_url if image_server_url.endswith('/') else image_server_url + '/'
        new_url = f"{base_url}{image_filename}"
        return f"![{alt_text}]({new_url})"

    # Regex to find local image markdown syntax: ![alt text](path)
    # (?!https?:\/\/) ensures it's not a web URL
    processed_markdown = re.sub(r"!\[(.*?)\]\((?!https?:\/\/)(.*?)\)", replace_image_path, markdown_content)

    tab1, tab2, tab3 = st.tabs(["Source", "Full", "Slide"])

    with tab1:
        st.text_area("Edit", markdown_content, height=600, label_visibility="collapsed")

    with tab2:
        st.markdown(markdown_content, unsafe_allow_html=True)

    with tab3:
        st.markdown(processed_markdown, unsafe_allow_html=True)