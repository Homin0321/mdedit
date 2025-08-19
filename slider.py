import streamlit as st
import re
import os

st.set_page_config(layout="wide")

def split_by_regex(regex, text):
    parts = []
    current_part = ""
    in_code_block = False
    in_table = False
    table_content = ""
    
    for line in text.splitlines():
        # Check for code block
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
        
        # Check for table
        if line.strip().startswith('|') or line.strip().startswith('+-'):
            if not in_table:
                in_table = True
            table_content += line + "\n"
        elif in_table and not line.strip():
            in_table = False
            current_part += table_content
            table_content = ""
        
        # Handle splitting
        if re.match(regex, line) and not in_code_block and not in_table:
            if current_part:
                parts.append(current_part)
                current_part = ""
            current_part += line + "\n"
        else:
            current_part += line + "\n"
    
    # Add any remaining content
    if current_part:
        parts.append(current_part)
    
    return parts

def split_by_lines(num, text):
    parts = []
    lines = text.splitlines()
    
    current_chunk = []
    in_table = False
    in_code_block = False
    chunk_line_count = 0
    
    for line in lines:
        # Check if line starts or ends a code block
        if line.strip().startswith('```'):
            in_code_block = not in_code_block
        
        # Check if line is part of a markdown table
        if line.strip().startswith('|') or line.strip().startswith('+-'):
            in_table = True
        elif in_table and not line.strip():
            in_table = False
        
        current_chunk.append(line)
        chunk_line_count += 1
        
        # Only split when we're not in a table or code block and have reached the line limit
        if chunk_line_count >= num and not in_table and not in_code_block:
            chunk_text = '\n'.join(current_chunk) + '\n'
            
            # If the last line is a heading, split before it
            if is_markdown_heading(current_chunk[-1]):
                split_chunks = split_at_last_heading(chunk_text)
                parts.extend(split_chunks[:-1])  # Add all but the last chunk
                current_chunk = [split_chunks[-1].strip()]  # Start new chunk with the heading
            else:
                parts.append(chunk_text)
                current_chunk = []
            
            chunk_line_count = len(current_chunk)
    
    # Add any remaining lines
    if current_chunk:
        parts.append('\n'.join(current_chunk) + '\n')
    
    return parts

@st.cache_data
def split_content(text):
    parts = [text]
    
    if st.session_state.separator_page_length:
        parts = split_by_lines(st.session_state.page_lines, text)
    
    if st.session_state.separator_hr:
        parts_gen = (part for page in parts for part in split_by_regex(r'---\s*$', page))
        parts = [re.sub(r'---\s*\n', '', part).strip() + '\n' for part in parts_gen]
        parts = [segment.strip() + '\n' for segment in parts]

    if st.session_state.separator_h1:
        parts = [part for page in parts for part in split_by_regex(r'^# .*$', page)]
    
    if st.session_state.separator_h2:
        parts = [part for page in parts for part in split_by_regex(r'^## .*$', page)]
    
    if st.session_state.separator_h3:
        parts = [part for page in parts for part in split_by_regex(r'^### .*$', page)]
    
    if st.session_state.separator_bold:
        parts = [part for page in parts for part in split_by_regex(r'^\*\*(.*?)\*\*$', page)]
    
    if len(parts) > 1:
        return parts
    else:
        return [text]

def resplit():
    # Clear the current page when changing separators
    st.session_state.current_page = 0
    # Clear the cached split content to force a recalculation
    split_content.clear()

def update_slider():
    page = st.session_state.page_slider -1
    if page != st.session_state.current_page:
        st.session_state.current_page = page

def is_markdown_heading(line):
    # Check if line is a markdown heading (level 1, 2, or 3)
    stripped_line = line.strip()
    return (
            stripped_line.startswith('#') or 
            stripped_line.startswith('##') or 
            stripped_line.startswith('###') or 
            stripped_line.startswith('####'))

def split_at_last_heading(text):
    lines = text.splitlines()
    last_heading_index = -1
    
    # Find the last heading in the text
    for i, line in enumerate(lines):
        if is_markdown_heading(line):
            last_heading_index = i
    
    # If a heading was found and it's not the first line
    if last_heading_index > 0:
        part1 = '\n'.join(lines[:last_heading_index]) + '\n'
        part2 = '\n'.join(lines[last_heading_index:]) + '\n'
        return [part1, part2]
    
    return ['\n'.join(lines) + '\n']

def remove_decorators(text):
    # Remove leading hashes
    text = text.lstrip('#')

    # Remove bold formatting
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)

    # Remove trailing colon
    if text.endswith(':'):
        text = text[:-1]

    return text

def find_index(lst, target):
    # Finds the index of a target item in a list
    for i, str in enumerate(lst):
        if str == target:
            return i
    return -1

@st.dialog("Page Index", width="large")
def show_index(toc):
    idx = st.session_state.current_page
    
    def format_func(item):
        return item[:60] + ("..." if len(item) > 60 else "")

    selected = st.radio(
        "Contents:",
        toc,
        index=idx,
        format_func=format_func,
        label_visibility="collapsed"
    )
    if selected is not None:
        idx = find_index(toc, selected)
        if idx != -1 and st.session_state.current_page != idx:
            st.session_state.current_page = idx
            st.rerun()

@st.cache_data
def make_index(pages):
    index = []
    for i, page in enumerate(pages):
        first_line = remove_decorators(page.strip().split('\n')[0])
        first_line = f"{i+1}. {first_line}"
        index.append(first_line)
    return index


# Main
st.session_state.text = st.session_state.get("text", "")
st.session_state.current_page = st.session_state.get("current_page", 0)
st.session_state.separator = st.session_state.get("separator", "Page length")
st.session_state.page_lines = st.session_state.get("page_lines", 20)
st.session_state.separator_hr = st.session_state.get("separator_hr", True)
st.session_state.separator_h1 = st.session_state.get("separator_h1", False)
st.session_state.separator_h2 = st.session_state.get("separator_h2", False)
st.session_state.separator_h3 = st.session_state.get("separator_h3", False)
st.session_state.separator_h4 = st.session_state.get("separator_h4", False)
st.session_state.separator_bold = st.session_state.get("separator_bold", False)
st.session_state.separator_page_length = st.session_state.get("separator_page_length", False)
st.session_state.markdown_content = st.session_state.get("markdown_content", "")
st.session_state.last_uploaded_file_id = st.session_state.get("last_uploaded_file_id", None)

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
    if st.session_state.get('last_uploaded_file_id') != uploaded_md_file.file_id:
        st.session_state.markdown_content = uploaded_md_file.getvalue().decode("utf-8")
        st.session_state.last_uploaded_file_id = uploaded_md_file.file_id

    def replace_image_path(match):
        alt_text = match.group(1)
        original_path = match.group(2)
        image_filename = os.path.basename(original_path)
        base_url = image_server_url if image_server_url.endswith('/') else image_server_url + '/'
        new_url = f"{base_url}{image_filename}"
        return f"![{alt_text}]({new_url})"

    # Regex to find local image markdown syntax: ![alt text](path)
    # (?!https?:\\/\/) ensures it's not a web URL
    processed_markdown = re.sub(r"!\[(.*?)\]\((?!https?://)(.*?)\)", replace_image_path, st.session_state.markdown_content)

    tab1, tab2, tab3 = st.tabs(["Source", "One Page", "Slides"])

    with tab1:
        st.text_area("Edit", key="markdown_content", height=600, label_visibility="collapsed")

    with tab2:
        st.markdown(processed_markdown, unsafe_allow_html=True)

    with tab3:
        pages = split_content(processed_markdown)
        index = make_index(pages)

        placeholder = st.empty()
        st.divider()

        col1, col2, col3, col4, col5 = st.columns([1, 1, 8, 1, 1])

        with col1:
            if st.button("◀", use_container_width=True):
                if st.session_state.current_page == 0:
                    st.session_state.current_page = len(pages)-1
                else:
                    st.session_state.current_page -= 1

        with col2:
            if st.button("▶", use_container_width=True):
                if st.session_state.current_page == len(pages)-1:
                    st.session_state.current_page = 0
                else:
                    st.session_state.current_page += 1

        with col3:
            slider = st.empty()

        with col4:
            if st.button("Jump", use_container_width=True):
                show_index(index)

        with col5:
            with st.popover("Split"):
                st.checkbox(r"\\---", key="separator_hr", on_change=resplit)
                st.checkbox(r"\\#", key="separator_h1", on_change=resplit)
                st.checkbox(r"\\##", key="separator_h2", on_change=resplit)
                st.checkbox(r"\\###", key="separator_h3", on_change=resplit)
                st.checkbox(r"\\####", key="separator_h4", on_change=resplit)
                st.checkbox(r"\\** ~ **", key="separator_bold", on_change=resplit)
                st.checkbox("Page length", key="separator_page_length", on_change=resplit)
                st.slider("Select page length", min_value=1, max_value=30,
                            key="page_lines",
                            on_change=resplit)

        if len(pages) > 1:
            slider.slider("Go to", min_value=1, max_value=len(pages),
                            value=st.session_state.current_page + 1,
                            key="page_slider",
                            on_change=update_slider,
                            label_visibility="collapsed")

        slide_content = pages[st.session_state.current_page]

        placeholder.markdown(slide_content, unsafe_allow_html=True)
