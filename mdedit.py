import streamlit as st
import base64
import html
import os
import re
from datetime import datetime
from pathlib import Path
from md2pdf.core import md2pdf

UPLOADS_DIR = "uploads"

# Ensure the upload directory exists
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

def get_files_list():
    return sorted([f for f in os.listdir(UPLOADS_DIR) if os.path.isfile(os.path.join(UPLOADS_DIR, f))])

def load_file_content(selected_file):
    file_path = os.path.join(UPLOADS_DIR, selected_file)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            st.session_state.text = f.read()
        st.toast(f"File '{selected_file}' loaded successfully!", icon="✅")
    except Exception as e:
        st.toast(f"Error reading file '{selected_file}': {e}", icon="🚫")

def save_text_file(silent_mode):
    file_name = st.session_state.file_name if st.session_state.file_name.endswith('.md') else st.session_state.file_name + '.md'
    file_content = st.session_state.text
    try:
        with open(os.path.join(UPLOADS_DIR, file_name), "w", encoding="utf-8") as f:
            f.write(file_content)
        if silent_mode is not True:
            st.toast(f"File '{file_name}' saved successfully!", icon="✅")
        update_last_modified(file_name)
    except Exception as e:
        st.toast(f"Error saving file '{file_name}': {e}", icon="🚫")

@st.fragment(run_every="60s")
def auto_save():
    if st.session_state.file_name:
        save_text_file(silent_mode=True)

def export_to_pdf():
    output_file = st.session_state.file_name + '.pdf'
    try:
        md2pdf(output_file, st.session_state.text)
        with open(output_file, "rb") as file:
            st.download_button(label="Download PDF",
                data=file,
                file_name=output_file,
                mime="application/pdf",
                use_container_width=True)
        os.remove(output_file)
        st.toast(f"File '{output_file}' saved successfully!", icon="✅")
    except Exception as e:
        st.toast(f"Error exporting file '{output_file}': {e}", icon="🚫")

def create_new_file():
    new_file_name = st.session_state.new_file
    if new_file_name:
        new_file_name = new_file_name if new_file_name.endswith('.md') else new_file_name + '.md'
        if os.path.exists(os.path.join(UPLOADS_DIR, new_file_name)):
            st.toast("File already exists. Choose a different name.", icon="⚠️")
        else:
            st.session_state.file_name = os.path.splitext(new_file_name)[0]
            st.session_state.text = ""
            st.session_state.new_file = ""
            save_text_file(silent_mode=True)
            resplit()
            st.toast(f"New file '{new_file_name}' created successfully!", icon="✅")

def rename_file():
    old_file_name = st.session_state.file_name + '.md'
    new_file_name = st.session_state.rename_file + '.md'
    if new_file_name != old_file_name:
        old_file_path = os.path.join(UPLOADS_DIR, old_file_name)
        new_file_path = os.path.join(UPLOADS_DIR, new_file_name)

        if os.path.exists(new_file_path):
            st.toast("A file with the new name already exists.", icon="⚠️")
            return
        
        try:
            os.rename(old_file_path, new_file_path)
            st.toast(f"File renamed to '{new_file_name}' successfully!", icon="✅")
            st.session_state.file_name = os.path.splitext(new_file_name)[0]
            update_last_modified(new_file_name)
        except Exception as e:
            st.toast(f"Error renaming file: {e}", icon="🚫")
    else:
        st.warning("The new file name is the same as the current one.")

def delete_file():
    file_name = st.session_state.file_name + '.md'
    try:
        os.remove(os.path.join(UPLOADS_DIR, file_name))
        st.toast(f"File '{file_name}' deleted successfully!", icon="✅")
        st.session_state.file_name = ""
        st.session_state.text = ""
    except Exception as e:
        st.toast(f"Error deleting file '{file_name}': {e}", icon="🚫")

def open_file():
    selected_file = st.session_state.open_file
    if selected_file:
        load_file_content(selected_file)
        st.session_state.file_name = os.path.splitext(selected_file)[0]
        resplit()

def upload_file():
    uploaded_file = st.session_state.upload_file
    if uploaded_file:
        st.session_state.file_name = os.path.splitext(uploaded_file.name)[0]
        try:
            st.session_state.text = uploaded_file.read().decode("utf-8")
            save_text_file(silent_mode=True)
            resplit()
            st.toast(f"File '{uploaded_file.name}' uploaded successfully!", icon="✅")
        except Exception as e:
            st.toast(f"Error uploading file: {e}", icon="🚫")

def update_last_modified(file_name):
    last_modified = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.last_modified = last_modified

def get_word_count(text):
    return len(re.findall(r'\w+', text))

def get_line_count(text):
    return text.count('\n') + 1

def markdown_images(markdown):
    # ![Test image](images/test.png "Alternate text")
    images = re.findall(r'(!\[(?P<image_title>[^\]]+)\]\((?P<image_path>[^\)"\s]+)\s*([^\)]*)\))', markdown)
    return images

def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

def img_to_html(img_path, img_alt):
    img_format = img_path.split(".")[-1]
    img_html = f'<img src="data:image/{img_format.lower()};base64,{img_to_bytes(img_path)}" alt="{img_alt}" style="max-width: 100%;">'
    return img_html

def markdown_insert_images(markdown):
    images = markdown_images(markdown)

    for image in images:
        image_markdown = image[0]
        image_alt = image[1]
        image_path = image[2]
        if os.path.exists(image_path):
            markdown = markdown.replace(image_markdown, img_to_html(image_path, image_alt))
    return markdown

@st.cache_data
def create_toc(text):
    headers = re.findall(r'^(#{1,6})\s+(.+)$', text, re.MULTILINE)
    if headers:
        toc = "<div style='background-color: #f0f0f0; padding: 10px; border-radius: 5px;'>"
        toc += "<ul style='list-style-type: none; padding-left: 0;'>"
        for i, header in enumerate(headers):
            level = len(header[0])
            title = remove_decorators(html.escape(header[1]))
            link = f"header-{i}"
            toc += f"<li style='margin-left: {(level-1)*20}px;'>"
            toc += f"<a href='#{link}' style='text-decoration: none; color: #333;'>"
            toc += f"{'•' if level > 1 else ''}  {title}</a></li>"
        toc += "</ul></div>"

        content = text
        for i, header in enumerate(headers):
            old_header = f"{header[0]} {header[1]}"
            new_header = f"{header[0]} <a id='header-{i}'></a>{header[1]}"
            content = content.replace(old_header, new_header, 1)

        return toc, content
    else:
        return None, text

@st.dialog("Found Results", width="large")
def highlight_matches(regex):
    try:
        pattern = re.compile(regex)
        content = st.session_state.text
        for match in reversed(list(pattern.finditer(st.session_state.text))):
            start, end = match.span()
            content = f"{content[:start]}<span style='background-color: yellow;'>{content[start:end]}</span>{content[end:]}"
        st.markdown(content, unsafe_allow_html=True)
    except re.error:
        st.toast("Invalid regular expression. Please check your input.")

def replace_all_matches(text, regex, replace):
    try:
        return re.sub(regex, replace, text)
    except re.error:
        st.error("Invalid regular expression. Please check your input.")
        return text

def split_by_regex(regex, text):
    parts = []
    current_part = ""
    for line in text.splitlines():
        if re.match(regex, line):
            if current_part:
                parts.append(current_part)
                current_part = ""
            current_part += line + "\n"
        else:
            current_part += line + "\n"
    if current_part:
        parts.append(current_part)

    return parts

def is_markdown_heading(line):
    # Check if line is a markdown heading (level 1, 2, or 3)
    stripped_line = line.strip()
    return (stripped_line.startswith('#') or 
            stripped_line.startswith('##') or 
            stripped_line.startswith('###'))

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
        parts = [part for page in parts for part in split_by_regex(r'\n---\n', page)]
    
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
    selected = st.radio("Contents:", toc, index=idx, label_visibility="collapsed")
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

def update_slider():
    page = st.session_state.page_slider -1
    if page != st.session_state.current_page:
        st.session_state.current_page = page

def main():
    st.set_page_config(layout="wide", page_title="Markdown Editor", page_icon="📝")

    st.session_state.text = st.session_state.get("text", "")
    st.session_state.file_name = st.session_state.get("file_name", "")
    st.session_state.height = st.session_state.get("height", 600)
    st.session_state.current_page = st.session_state.get("current_page", 0)
    st.session_state.separator = st.session_state.get("separator", "Page length")
    st.session_state.page_lines = st.session_state.get("page_lines", 20)

    st.session_state.separator_hr = st.session_state.get("separator_hr", True)
    st.session_state.separator_h1 = st.session_state.get("separator_h1", True)
    st.session_state.separator_h2 = st.session_state.get("separator_h2", True)
    st.session_state.separator_h3 = st.session_state.get("separator_h3", False)
    st.session_state.separator_bold = st.session_state.get("separator_bold", False)
    st.session_state.separator_page_length = st.session_state.get("separator_page_length", False)

    with st.sidebar:
        if st.session_state.file_name:
            st.subheader(st.session_state.file_name + '.md')
        else:
            st.subheader("No File Selected")

        st.text_input("New File:", key="new_file", on_change=create_new_file, placeholder="Enter new file name")

        files = get_files_list()
        if files:
            st.selectbox("Open File:", files, index=None, key="open_file", on_change=open_file)

        if st.session_state.file_name:
            st.text_input("Rename File:", st.session_state.file_name, key="rename_file", on_change=rename_file)

            if st.button("Delete File", use_container_width=True):
                delete_file()

            if st.button("Save File", use_container_width=True):
                save_text_file(silent_mode=False)

            output_file = st.session_state.file_name if st.session_state.file_name.endswith('.md') else st.session_state.file_name + '.md'
            try:
                if st.download_button(label="Download File",
                    data=st.session_state.text,
                    file_name=output_file,
                    mime="text/markdown",
                    use_container_width=True):
                    st.toast(f"File '{output_file}' saved successfully!", icon="✅")
            except Exception as e:
                st.toast(f"Error exporting file '{output_file}': {e}", icon="🚫")

            if st.button("Export to PDF", use_container_width=True):
                export_to_pdf()

        with st.expander("Upload File"):
            st.file_uploader(" ", type=["md", "txt"], key="upload_file", on_change=upload_file)

        if st.session_state.file_name:
            if hasattr(st.session_state, 'last_modified'):
                st.write(f"Last modified: {st.session_state.last_modified}")
            st.write(f"{get_word_count(st.session_state.text)} words, {get_line_count(st.session_state.text)} lines")
            st.session_state.height = st.slider("Text Box Height:", 100, 1000, 600, 100)

    tab1, tab2, tab3 = st.tabs(["Edit", "Preview", "Slide"])

    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            regex = st.text_input(" ", placeholder="Regular Expression", label_visibility="collapsed")
        with col2:
            find_all = st.button("Find All", use_container_width=True)
        with col3:
            replace = st.text_input(" ", placeholder="Replacing Text", label_visibility="collapsed")
        with col4:
            replace_all = st.button("Replace All", use_container_width=True)
        
        if find_all:
            highlight_matches(regex)
        if replace_all:
            try:
                st.session_state.text = re.sub(regex, replace, st.session_state.text)
            except re.error:
                st.toast("Invalid regular expression. Please check your input.")

        st.text_area("Edit:", key="text", height=st.session_state.height, label_visibility="collapsed")

    with tab2:
        toc, content = create_toc(st.session_state.text)
        if toc:
            with st.popover("Table of Contents"):
                st.markdown(toc, unsafe_allow_html=True)
        
        with st.container(border=False, height=st.session_state.height):
            content = markdown_insert_images(content)
            st.markdown(content, unsafe_allow_html=True)

    with tab3:
        pages = split_content(st.session_state.text)
        index = make_index(pages)

        placeholder = st.empty()
        st.divider()

        col1, col2, col3, col4, col5 = st.columns([1, 1, 9, 1, 1])

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
            if st.button("Jump to", use_container_width=True):
                show_index(index)

        with col5:
            with st.popover("Split by"):
                st.checkbox("\---", key="separator_hr", on_change=resplit)
                st.checkbox("\#", key="separator_h1", on_change=resplit)
                st.checkbox("\##", key="separator_h2", on_change=resplit)
                st.checkbox("\###", key="separator_h3", on_change=resplit)
                st.checkbox("\** ~ **", key="separator_bold", on_change=resplit)
                st.checkbox("Page length", key="separator_page_length", on_change=resplit)
                st.slider("Select page length", min_value=1, max_value=30,
                            value=20,
                            key="page_lines",
                            on_change=resplit)

        if len(pages) > 1:
            slider.slider("Go to", min_value=1, max_value=len(pages),
                            value=st.session_state.current_page + 1,
                            key="page_slider",
                            on_change=update_slider,
                            label_visibility="collapsed")

        placeholder.markdown(pages[st.session_state.current_page], unsafe_allow_html=True)

    auto_save()
    
if __name__ == "__main__":
    main()