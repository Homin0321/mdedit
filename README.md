# Streamlit Markdown Editor

This is a simple Markdown editor built with Streamlit. It allows users to create, edit, save, and preview Markdown files directly in the browser.

## Features

- Create new Markdown files
- Open existing files
- Edit files in a text area
- Preview rendered Markdown
- Save files
- Rename files
- Delete files
- Upload files
- Word count
- Last modified timestamp

## Requirements

- Python 3.6+
- Streamlit
- pytz

## Installation

1. Clone this repository or download the source code.
2. Install the required packages:

```
pip install streamlit pytz
```

## Usage

Run the Streamlit app with:

```
streamlit run app.py
```

Replace `app.py` with the name of the Python file containing the code.

## How it works

1. The app creates an `uploads` directory to store Markdown files.
2. The sidebar provides options for file management:
   - Create a new file
   - Open an existing file
   - Rename the current file
   - Upload a file
   - Delete the current file
   - Save the current file
3. The main area is split into two tabs:
   - Edit: A text area for editing the Markdown content
   - Preview: A rendered view of the Markdown content
4. The app tracks the last modified time and word count for the current file.

## File Management

- **New File**: Enter a name and press Enter to create a new file.
- **Open File**: Select a file from the dropdown to open it.
- **Rename File**: Enter a new name and press Enter to rename the current file.
- **Upload File**: Use the file uploader to upload a Markdown or text file.
- **Delete File**: Click the "Delete File" button to remove the current file.
- **Save File**: Click the "Save File" button to save changes to the current file.

## Notes

- All files are saved with a `.md` extension.
- The app uses UTF-8 encoding for file operations.
- Error handling is implemented with toast notifications for user feedback.

## License

This project is licensed under the MIT License.
