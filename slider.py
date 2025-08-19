import streamlit as st
import re
import base64
import os # For os.path.basename

st.set_page_config(layout="wide")

with st.sidebar:
    st.title("마크다운 및 이미지 파일 업로더")
    uploaded_files = st.file_uploader(
        "마크다운 파일과 참조된 이미지 파일들을 함께 업로드하세요.",
        type=["md", "png", "jpg", "jpeg", "gif", "bmp", "webp"], # Added more image types
        accept_multiple_files=True
    )

if uploaded_files: # Check if any files are uploaded
    markdown_content = None
    image_files = {}

    for file in uploaded_files:
        if file.name.endswith('.md'):
            markdown_content = file.getvalue().decode("utf-8")
        elif file.type.startswith('image/'):
            image_files[os.path.basename(file.name)] = file # Store image files by their base name

    if markdown_content is None:
        st.error("마크다운 파일이 업로드되지 않았습니다. 마크다운 파일을 포함하여 업로드해주세요.")
    else:
        # Function to replace local image paths with base64 data URIs
        def replace_local_image_with_base64(match):
            original_path = match.group(2) # The path inside the parentheses
            # Extract just the filename from the path (e.g., 'images/pic.png' -> 'pic.png')
            image_filename = os.path.basename(original_path)

            if image_filename in image_files:
                img_file = image_files[image_filename]
                img_bytes = img_file.getvalue()
                img_base64 = base64.b64encode(img_bytes).decode("utf-8")
                mime_type = img_file.type
                return f"![{match.group(1)}](data:{mime_type};base64,{img_base64})"
            else:
                # If image not found among uploaded files, keep original path
                return match.group(0) # Return the whole matched string

        # Regex to find image markdown syntax: ![alt text](path)
        # (?!https?:\/\/) ensures it's not a web URL
        # This regex captures the alt text (group 1) and the path (group 2)
        processed_markdown = re.sub(r"!\[(.*?)](?!https?:\/\/)(.*?)\)", replace_local_image_with_base64, markdown_content)

        st.markdown("### 업로드된 마크다운 파일:")
        st.markdown(processed_markdown, unsafe_allow_html=True)
