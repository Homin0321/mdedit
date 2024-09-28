import streamlit as st
import os

# Constants
UPLOADS_DIR = "uploads"

# Ensure the upload directory exists
if not os.path.exists(UPLOADS_DIR):
    os.makedirs(UPLOADS_DIR)

# Helper functions
def get_files_list():
    """Returns a list of files in the UPLOADS_DIR."""
    return [f for f in os.listdir(UPLOADS_DIR) if os.path.isfile(os.path.join(UPLOADS_DIR, f))]

def load_file_content(selected_file):
    """Loads the content of the selected file into session state."""
    file_path = os.path.join(UPLOADS_DIR, selected_file)
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            st.session_state.text = f.read()
        st.success(f"File '{selected_file}' loaded successfully!")
    except Exception as e:
        st.error(f"Error reading file '{selected_file}': {e}")

def save_text_file():
    """Saves the text in the editor to a file."""
    if 'file_name' not in st.session_state or not st.session_state.file_name:
        st.error("Please provide a valid file name.")
        return

    file_name = st.session_state.file_name + '.md'
    file_content = st.session_state.text

    try:
        with open(os.path.join(UPLOADS_DIR, file_name), "w", encoding="utf-8") as f:
            f.write(file_content)
        st.success(f"File '{file_name}' saved successfully!")
    except Exception as e:
        st.error(f"Error saving file '{file_name}': {e}")

def create_new_file():
    """Creates a new file by clearing session state."""
    new_file_name = st.session_state.new_file
    if new_file_name:
        if os.path.exists(os.path.join(UPLOADS_DIR, new_file_name + '.md')):
            st.error("File already exists. Choose a different name.")
        else:
            st.session_state.file_name = new_file_name
            st.session_state.text = ""
            st.session_state.new_file = ""
            st.success(f"New file '{new_file_name}.md' created successfully!")

def rename_file():
    """Renames the current file."""
    old_file_name = st.session_state.file_name + '.md'
    new_file_name = st.session_state.rename_file + '.md'
    
    if new_file_name != old_file_name:
        old_file_path = os.path.join(UPLOADS_DIR, old_file_name)
        new_file_path = os.path.join(UPLOADS_DIR, new_file_name)

        if os.path.exists(new_file_path):
            st.error("A file with the new name already exists.")
            return
        
        try:
            os.rename(old_file_path, new_file_path)
            st.success(f"File renamed to '{new_file_name}' successfully!")
            st.session_state.file_name = os.path.splitext(new_file_name)[0]
        except Exception as e:
            st.error(f"Error renaming file: {e}")
    else:
        st.warning("The new file name is the same as the current one.")

def delete_file():
    """Deletes the current file after confirmation."""
    file_name = st.session_state.file_name + '.md'
    if st.checkbox(f"Confirm delete '{file_name}'?"):
        try:
            os.remove(os.path.join(UPLOADS_DIR, file_name))
            st.success(f"File '{file_name}' deleted successfully!")
            st.session_state.file_name = ""
            st.session_state.text = ""
        except Exception as e:
            st.error(f"Error deleting file '{file_name}': {e}")

def open_file():
    """Loads the selected file."""
    selected_file = st.session_state.open_file
    if selected_file:
        load_file_content(selected_file)
        st.session_state.file_name = os.path.splitext(selected_file)[0]

def upload_file():
    """Handles the file upload process."""
    uploaded_file = st.session_state.upload_file
    if uploaded_file:
        st.session_state.file_name = os.path.splitext(uploaded_file.name)[0]
        try:
            st.session_state.text = uploaded_file.read().decode("utf-8")
            st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        except Exception as e:
            st.error(f"Error uploading file: {e}")

# Initialize session state variables
if 'text' not in st.session_state:
    st.session_state.text = ""
if 'file_name' not in st.session_state:
    st.session_state.file_name = ""

# Page configuration
st.set_page_config(layout="wide", page_title="Markdown Editor", page_icon="📝")

# Display current file name if available
if st.session_state.file_name:
    st.subheader(f"Editing: {st.session_state.file_name}.md")

# Tabs
tab1, tab2, tab3 = st.tabs(["File", "Edit", "Preview"])

# Tab 1: File Operations
with tab1:
    st.text_input("New File Name:", key="new_file", on_change=create_new_file, placeholder="Enter new file name")

    files = get_files_list()
    if files:
        st.selectbox("Open File:", files, index=None, key="open_file", on_change=open_file)

    if st.session_state.file_name:
        st.text_input("Rename Current File:", st.session_state.file_name, key="rename_file", on_change=rename_file)

    st.file_uploader("Upload Markdown File:", type=["md", "txt"], key="upload_file", on_change=upload_file)

    if st.button("Save File"):
        save_text_file()

    if st.session_state.file_name and st.button("Delete File"):
        delete_file()

# Tab 2: Markdown Editor
with tab2:
    st.text_area("Edit Markdown:", key="text", height=800)

# Tab 3: Markdown Preview
with tab3:
    st.markdown(st.session_state.text)