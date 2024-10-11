# Markdown Editor

A feature-rich Streamlit web application for creating, editing, and managing Markdown documents with advanced features like live preview, table of contents generation, and presentation mode.

## Features

- **File Management**
  - Create, open, rename, and delete Markdown files
  - Upload and download Markdown files
  - Export to PDF
  - Auto-save functionality

- **Editor**
  - Regular expression search and replace
  - Adjustable editor height
  - Word and line count
  - Image embedding support

- **Preview**
  - Live Markdown rendering
  - Automatic table of contents generation
  - Support for embedded images

- **Presentation Mode**
  - Split content into slides based on various separators:
    - Page length
    - Markdown headings (# / ## / ###)
    - Horizontal rules (---)
    - Bold text markers (** ~ **)
  - Navigation controls
  - Slide index for quick jumping

## Requirements

```
streamlit
md2pdf
```

## Usage

1. Run the application:
   ```
   streamlit run app.py
   ```

2. The interface is divided into three main tabs:
   - **Edit**: Text editor with search and replace functionality
   - **Preview**: Live rendering of Markdown content with table of contents
   - **Slide**: Presentation mode for viewing content as slides

3. Use the sidebar for file management:
   - Create new files
   - Open existing files
   - Rename or delete current file
   - Download Markdown or export to PDF
   - Upload files
   - Adjust editor height

## File Structure

The application creates an `uploads` directory to store Markdown files. All files are saved with `.md` extension.

## Key Functions

### Content Splitting
- `split_by_regex(regex, text)`: Splits content based on regular expressions
- `split_by_lines(num, text)`: Splits content by number of lines
- `is_markdown_heading(line)`: Checks if a line is a Markdown heading

### Content Processing
- `create_toc(text)`: Generates a table of contents
- `markdown_insert_images(markdown)`: Processes and embeds images
- `remove_decorators(text)`: Cleans text for index display

### File Operations
- `save_text_file(silent_mode)`: Saves the current content
- `load_file_content(selected_file)`: Loads content from a file
- `export_to_pdf()`: Exports the current content to PDF

## Notes

- The application automatically saves content every 60 seconds
- Images are embedded directly in the Markdown preview
- The presentation mode remembers the current page between tab switches

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License