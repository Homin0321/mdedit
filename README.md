# Markdown Editor

This is a simple Markdown editor built with Streamlit. It allows you to create, edit, save, and export Markdown files to PDF.

## Features

- **Create new Markdown files:** Easily create new files with a user-friendly interface.
- **Open existing files:** Load and edit existing Markdown files from the `uploads` directory.
- **Save files:** Save your changes to the `uploads` directory.
- **Export to PDF:** Convert your Markdown files to PDF format for easy sharing and printing.
- **Rename files:** Rename existing files.
- **Delete files:** Delete files from the `uploads` directory.
- **Upload files:** Upload Markdown files from your local machine.
- **Find and Replace:** Use regular expressions to find and replace text within your Markdown files.
- **Markdown Preview:** View a live preview of your Markdown content with support for images and a table of contents.
- **Word and Line Count:** Get the word and line count of your Markdown file.

## Installation

1. Install Streamlit:
   ```bash
   pip install streamlit
   ```

2. Install the `md2pdf` library:
   ```bash
   pip install md2pdf
   ```

## Usage

1. Run the app:
   ```bash
   streamlit run app.py
   ```

2. Use the sidebar to create, open, save, export, rename, delete, and upload files.
3. Edit your Markdown content in the "Edit" tab.
4. Preview your Markdown content in the "Preview" tab.

## License

This project is licensed under the MIT License

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [md2pdf](https://pypi.org/project/md2pdf/)