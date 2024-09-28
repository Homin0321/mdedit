# Markdown Editor

This Streamlit app provides a simple yet powerful Markdown editor for creating and managing Markdown files.

## Features

- **File Management:**
    - Create new Markdown files.
    - Open existing Markdown files.
    - Rename files.
    - Delete files.
    - Upload files from your local machine.
- **Editing:**
    - A text area for editing Markdown content.
    - A slider to adjust the text area height.
- **Preview:**
    - A preview pane that renders the Markdown content in real-time.
    - A table of contents (TOC) for easy navigation within the document.
- **Word Count:**
    - Displays the word count of the current document.
- **Last Modified:**
    - Shows the last modified timestamp of the current file.

## Usage

1. **Run the app:**
   - Make sure you have Streamlit installed (`pip install streamlit`).
   - Run the script: `streamlit run markdown_editor.py`
2. **Interact with the app:**
   - Use the sidebar to create, open, rename, delete, or upload files.
   - Edit the Markdown content in the "Edit" tab.
   - View the rendered Markdown in the "Preview" tab.

## Requirements

- Python 3.7 or higher
- Streamlit

## Installation

1. Install Python 3.7 or higher.
2. Install Streamlit: `pip install streamlit`

## Running the App

1. Save the code as `markdown_editor.py`.
2. Open a terminal and navigate to the directory where you saved the file.
3. Run the following command: `streamlit run markdown_editor.py`

## Notes

- The app stores uploaded and created files in a directory named "uploads" within the same directory as the script.
- The app uses Streamlit's `st.cache_data` decorator to cache the TOC generation, improving performance.
- The app uses HTML and CSS for styling the TOC and preview pane.

## Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
