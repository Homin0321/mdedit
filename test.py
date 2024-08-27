import streamlit as st
import os

# Define a constant for the uploads directory
UPLOADS_DIR = "uploads"

def initialize_uploads_directory():
    """Ensure the uploads directory exists."""
    os.makedirs(UPLOADS_DIR, exist_ok=True)

def get_files_list():
    """Retrieve a list of files in the uploads directory."""
    return [f for f in os.listdir(UPLOADS_DIR) if os.path.isfile(os.path.join(UPLOADS_DIR, f))]

def display_files_list(files):
    """Display a selectbox for the user to choose a file from the uploads directory."""
    if files:
        selected_file = st.selectbox("Choose a file", files)
        return selected_file
    else:
        st.write("No files found in the directory.")
        return None

def display_file_content(file_path):
    """Display the content of the selected file in a text area."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
        st.text_area("File Content", file_content, height=200)
    except Exception as e:
        st.error(f"Error reading file: {e}")

def save_text_file(file_content, filename):
    """Save the uploaded content to a file with the specified filename."""
    try:
        with open(os.path.join(UPLOADS_DIR, filename), "w", encoding="utf-8") as f:
            f.write(file_content)
        st.success(f"File '{filename}' saved successfully!")
    except Exception as e:
        st.error(f"Error saving file: {e}")

def delete_file(filename):
    """Delete a file from the uploads directory."""
    try:
        os.remove(os.path.join(UPLOADS_DIR, filename))
        st.success(f"File '{filename}' deleted successfully!")
    except Exception as e:
        st.error(f"Error deleting file: {e}")

def file_uploader_and_saver():
    """Handle the file upload and saving process."""
    uploaded_file = st.file_uploader("Choose a text file", type=["md", "txt"])
    if uploaded_file is not None:
        # Read the file content
        file_content = uploaded_file.read().decode("utf-8")
        
        # Display the file content
        st.text_area("Uploaded File Content", file_content, height=200)

        # Get the filename
        filename = uploaded_file.name

        # Get new filename from user input
        new_filename = st.text_input("Enter new filename (optional):", filename)

        # Save the file button
        if st.button("Save File"):
            save_text_file(file_content, new_filename)

def file_operations(selected_file):
    """Provide options to delete or rename the selected file."""
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

# Main application logic
def main():
    st.title("File Manager")

    initialize_uploads_directory()

    st.write("## Saved Files:")
    files = get_files_list()
    selected_file = display_files_list(files)

    if selected_file:
        file_path = os.path.join(UPLOADS_DIR, selected_file)
        display_file_content(file_path)
        file_operations(selected_file)

    st.write("## Upload New File:")
    file_uploader_and_saver()

if __name__ == "__main__":
    main()