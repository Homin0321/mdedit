import streamlit as st
import os

UPLOADS_DIR = "uploads"

def get_files_list():
    return [f for f in os.listdir(UPLOADS_DIR) if os.path.isfile(os.path.join(UPLOADS_DIR, f))]

def load_file_content(selected_file):
    file_path = os.path.join(UPLOADS_DIR, selected_file)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            st.session_state.text = f.read()
    except Exception as e:
        st.error(f"Error reading file: {e}")

def save_text_file():
    file_name = st.session_state.file_name + '.md'
    file_content = st.session_state.text
    try:
        with open(os.path.join(UPLOADS_DIR, file_name), "w", encoding="utf-8") as f:
            f.write(file_content)
        st.success(f"File '{filename}' saved successfully!")
    except Exception as e:
        st.error(f"Error saving file: {e}")

def file_operations(selected_file):
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Delete File"):
            delete_file(selected_file)
    with col2:
        new_filename = st.text_input("Rename File:", selected_file)
        if st.button("Rename"):
            if new_filename and new_filename != selected_file:
                try:
                    os.rename(os.path.join(UPLOADS_DIR, selected_file), os.path.join(UPLOADS_DIR, new_filename))
                    st.success(f"File '{selected_file}' renamed to '{new_filename}' successfully!")
                except Exception as e:
                    st.error(f"Error renaming file: {e}")

st.set_page_config(layout="wide", page_title="Markdown Editor", page_icon="📝")

st.session_state.text = st.session_state.get("text", "")
st.session_state.file_name = st.session_state.get("file_name", "")

if st.session_state.file_name != "":
    st.subheader(st.session_state.file_name + '.md')

tab1, tab2, tab3 = st.tabs(["File", "Edit", "Preview"])
with tab1:
    st.markdown("**New File**")
    col1, col2, col3 = st.columns(3)
    with col1:
        file_name = st.text_input("Enter new file name:", label_visibility="collapsed")
    with col2:
        if st.button("Create"):
            if file_name:
                st.session_state.file_name = file_name
                st.session_state.text = ""
            else:
                st.error("Please enter a file name.")
            st.rerun()

    st.markdown("**Open File**")
    col1, col2, col3 = st.columns(3)
    with col1:
        files = get_files_list()
        if files:
            selected_file = st.selectbox("Choose a file", files, label_visibility="collapsed")
        else:
            st.write("No files found in the directory.")
    with col2:
        if st.button("Open"):
            if selected_file:
                load_file_content(selected_file)
                st.session_state.file_name = os.path.splitext(selected_file)[0]
            else:
                st.error("No files found in the directory.")
            st.rerun()

    st.markdown("**Upload File**")
    col1, col2, col3 = st.columns(3)
    with col1:
        uploaded_file = st.file_uploader("Choose a text file", type=["md", "txt"])
        if uploaded_file is not None:
            file_name = uploaded_file.name
            file_content = uploaded_file.read().decode("utf-8")

            st.session_state.file_name = os.path.splitext(file_name)[0]
            st.session_state.text = file_content
            #st.rerun()

    st.markdown("**Save File**")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Save File"):
            save_text_file()
            st.rerun()

with tab2:
    st.text_area("Edit Markdown:", key="text", height=800)

with tab3:
    st.markdown(st.session_state.text)
