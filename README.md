# Streamlit Markdown Editor

A powerful and feature-rich Markdown editor built with Streamlit and enhanced with AI capabilities using Google's Generative AI.

## Features

- Create, edit, and manage Markdown files
- Real-time preview with table of contents
- File management (create, rename, delete, upload, download)
- Export to PDF
- AI-powered text operations (correction, composition, summarization, translation, etc.)
- Regular expression search and replace
- Slide view with customizable page splitting
- Auto-save functionality

## Requirements

- Python 3.7+
- Streamlit
- google-generativeai
- md2pdf

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/streamlit-markdown-editor.git
   cd streamlit-markdown-editor
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables:
   - Create a `.streamlit/secrets.toml` file in the project directory
   - Add your Google AI API key and password:
     ```
     api_key = "your_google_ai_api_key"
     passwd = "your_password"
     ```

## Usage

Run the Streamlit app:

```
streamlit run app.py
```

Navigate to the provided URL in your web browser to use the Markdown editor.

## Main Components

1. **Edit Tab**: Write and edit your Markdown content with regex search and replace functionality.
2. **Wizard Tab**: Utilize AI-powered text operations to enhance your content.
3. **Preview Tab**: View the rendered Markdown with an auto-generated table of contents.
4. **Slide Tab**: Navigate through your content in a slide-like view with customizable page splitting.

## File Management

- Create new files
- Open existing files
- Rename files
- Delete files
- Upload files
- Download files
- Export to PDF

## AI Features

Powered by Google's Generative AI, the editor offers various text operations:

- Grammar and spelling correction
- Text composition
- Summarization
- Key points extraction
- Translation (Korean and English)
- Markdown formatting

## Customization

- Adjust the text box height
- Customize page splitting in the Slide view

## Auto-save

The editor automatically saves your work every 60 seconds.

## Notes

- Ensure you have the necessary permissions to read and write files in the `uploads` directory.
- The AI features require a valid Google AI API key.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)