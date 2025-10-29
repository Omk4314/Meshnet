# Excel Row Processor - Streamlit App

A web application built with Streamlit that processes Excel files by removing specific rows (odd or even) while preserving the header row.

## Features

- **Bulk File Upload**: Upload multiple Excel files (.xlsx, .xls) at once
- **Row Deletion Options**: 
  - Delete odd-numbered rows (2nd, 4th, 6th...)
  - Delete even-numbered rows (3rd, 5th, 7th...)
- **Header Preservation**: Always keeps the first row (header) intact
- **Batch Processing**: Process up to 100 files simultaneously
- **Automatic Downloads**: 
  - Single file: Direct Excel download
  - Multiple files: ZIP archive with all processed files
- **File Size Management**: Configurable maximum file size (default 50MB)
- **Error Handling**: Comprehensive error handling with user feedback

## Live Demo

🚀 **[Try the live app here](https://your-app-name.streamlit.app)** (Replace with your actual Streamlit Cloud URL)

## Installation & Local Development

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Streamlit app:
```bash
streamlit run app.py
```

## Deployment

### Streamlit Cloud (Recommended)

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Select your repository
5. Deploy automatically

### Other Platforms

- **Railway**: Use the provided `railway.json`
- **Render**: Use the provided `render.yaml`
- **Heroku**: Use the provided `Procfile`

## Usage

1. **Upload Files**: Use the file uploader to select one or more Excel files
2. **Choose Option**: Select whether to delete odd or even rows
3. **Process**: Click the appropriate button to process all files
4. **Download**: Download the processed files (single file or ZIP archive)

## File Processing Logic

- **Header Row**: Always preserved (row 1)
- **Delete Odd Rows**: Removes rows 2, 4, 6, 8... (keeps 1, 3, 5, 7...)
- **Delete Even Rows**: Removes rows 3, 5, 7, 9... (keeps 1, 2, 4, 6, 8...)

## Configuration

The app includes configurable settings in the sidebar:
- Maximum file size (1-100 MB)
- Maximum number of files to process (1-100)

## Error Handling

The app handles various error scenarios:
- Empty files
- Files with only headers
- Large files exceeding size limits
- Processing errors
- File format issues

## Dependencies

- `streamlit`: Web app framework
- `pandas`: Data manipulation and Excel processing
- `openpyxl`: Excel file reading/writing (.xlsx files)
- `xlrd`: Excel file reading (.xls files)

## Example

If you have an Excel file with 10 rows:
- **Original**: Rows 1-10 (Row 1 is header)
- **Delete Odd**: Keep rows 1, 3, 5, 7, 9 (header + odd data rows)
- **Delete Even**: Keep rows 1, 2, 4, 6, 8, 10 (header + even data rows)

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License.