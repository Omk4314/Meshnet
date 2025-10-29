import streamlit as st
import pandas as pd
import zipfile
import io
import os
import tempfile
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Excel Row Processor",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .upload-section {
        background-color: #f0f2f6;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .success-message {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .error-message {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
    .info-box {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #bee5eb;
    }
</style>
""", unsafe_allow_html=True)

def process_excel_file(file_content, filename, delete_option):
    """
    Process a single Excel file according to the selected option.
    
    Args:
        file_content: The uploaded file content
        filename: Name of the file
        delete_option: 'odd' or 'even' - which rows to delete
    
    Returns:
        Processed DataFrame or None if error
    """
    try:
        # Read the Excel file
        df = pd.read_excel(file_content, engine='openpyxl')
        
        if df.empty:
            st.warning(f"File {filename} is empty. Skipping...")
            return None
        
        # Keep the first row (header) and process the rest
        if len(df) <= 1:
            st.warning(f"File {filename} has only one row (header). No rows to delete.")
            return df
        
        # Create a copy to avoid modifying the original
        processed_df = df.copy()
        
        # Delete rows based on the selected option
        if delete_option == "odd":
            # Delete odd-numbered rows (1-indexed, so rows 2, 4, 6, ...)
            # Since we're 0-indexed in pandas, we delete rows 1, 3, 5, ...
            rows_to_delete = list(range(1, len(processed_df), 2))
        else:  # even
            # Delete even-numbered rows (1-indexed, so rows 3, 5, 7, ...)
            # Since we're 0-indexed in pandas, we delete rows 2, 4, 6, ...
            rows_to_delete = list(range(2, len(processed_df), 2))
        
        # Drop the specified rows
        processed_df = processed_df.drop(rows_to_delete).reset_index(drop=True)
        
        logger.info(f"Processed {filename}: Deleted {len(rows_to_delete)} rows")
        return processed_df
        
    except Exception as e:
        st.error(f"Error processing {filename}: {str(e)}")
        logger.error(f"Error processing {filename}: {str(e)}")
        return None

def create_excel_bytes(df, filename):
    """
    Convert DataFrame to Excel bytes.
    
    Args:
        df: DataFrame to convert
        filename: Original filename for reference
    
    Returns:
        Bytes of the Excel file
    """
    try:
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Sheet1')
        output.seek(0)
        return output.getvalue()
    except Exception as e:
        st.error(f"Error creating Excel file for {filename}: {str(e)}")
        logger.error(f"Error creating Excel file for {filename}: {str(e)}")
        return None

def create_zip_file(processed_files):
    """
    Create a ZIP file containing all processed Excel files.
    
    Args:
        processed_files: List of tuples (filename, excel_bytes)
    
    Returns:
        Bytes of the ZIP file
    """
    try:
        zip_buffer = io.BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for filename, excel_bytes in processed_files:
                if excel_bytes is not None:
                    # Clean filename for ZIP entry
                    clean_filename = Path(filename).stem + "_processed.xlsx"
                    zip_file.writestr(clean_filename, excel_bytes)
        
        zip_buffer.seek(0)
        return zip_buffer.getvalue()
    except Exception as e:
        st.error(f"Error creating ZIP file: {str(e)}")
        logger.error(f"Error creating ZIP file: {str(e)}")
        return None

def main():
    """Main application function."""
    
    # Header
    st.markdown('<h1 class="main-header">📊 Excel Row Processor</h1>', unsafe_allow_html=True)
    
    # Sidebar for instructions
    with st.sidebar:
        st.markdown("## 📋 Instructions")
        st.markdown("""
        1. **Upload Excel files** (.xlsx or .xls)
        2. **Choose deletion option**:
           - Delete odd rows (2nd, 4th, 6th...)
           - Delete even rows (3rd, 5th, 7th...)
        3. **Process files** and download results
        
        **Note**: The first row (header) is always preserved.
        """)
        
        st.markdown("## ⚙️ Settings")
        max_file_size = st.slider("Max file size (MB)", 1, 100, 50)
        max_files = st.slider("Max files to process", 1, 100, 100)
    
    # Main content area
    st.markdown('<div class="upload-section">', unsafe_allow_html=True)
    
    # File upload
    st.markdown("### 📁 Upload Excel Files")
    uploaded_files = st.file_uploader(
        "Choose Excel files to process",
        type=['xlsx', 'xls'],
        accept_multiple_files=True,
        help="You can upload multiple files at once (up to 100 files)"
    )
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if uploaded_files:
        # Validate file count
        if len(uploaded_files) > max_files:
            st.error(f"Too many files! Maximum allowed: {max_files}. You uploaded: {len(uploaded_files)}")
            return
        
        # Check file sizes
        large_files = []
        for file in uploaded_files:
            file_size_mb = file.size / (1024 * 1024)
            if file_size_mb > max_file_size:
                large_files.append(f"{file.name} ({file_size_mb:.1f} MB)")
        
        if large_files:
            st.error(f"Files too large (max {max_file_size} MB): {', '.join(large_files)}")
            return
        
        # Display uploaded files info
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown(f"**📊 Uploaded {len(uploaded_files)} file(s):**")
        for file in uploaded_files:
            file_size_mb = file.size / (1024 * 1024)
            st.markdown(f"- {file.name} ({file_size_mb:.2f} MB)")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Deletion option selection
        st.markdown("### ⚙️ Choose Row Deletion Option")
        
        col1, col2 = st.columns(2)
        
        with col1:
            delete_odd = st.button("🗑️ Delete Odd Rows", help="Delete rows 2, 4, 6, 8... (keep header)")
        
        with col2:
            delete_even = st.button("🗑️ Delete Even Rows", help="Delete rows 3, 5, 7, 9... (keep header)")
        
        # Process files based on selection
        if delete_odd or delete_even:
            delete_option = "odd" if delete_odd else "even"
            
            # Show processing status
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            processed_files = []
            successful_files = 0
            
            # Process each file
            for i, uploaded_file in enumerate(uploaded_files):
                status_text.text(f"Processing {uploaded_file.name}...")
                
                # Process the file
                processed_df = process_excel_file(uploaded_file, uploaded_file.name, delete_option)
                
                if processed_df is not None:
                    # Convert to Excel bytes
                    excel_bytes = create_excel_bytes(processed_df, uploaded_file.name)
                    
                    if excel_bytes is not None:
                        processed_files.append((uploaded_file.name, excel_bytes))
                        successful_files += 1
                
                # Update progress
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Show results
            if successful_files > 0:
                st.markdown('<div class="success-message">', unsafe_allow_html=True)
                st.markdown(f"✅ **Successfully processed {successful_files} out of {len(uploaded_files)} files!**")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Download section
                st.markdown("### 📥 Download Processed Files")
                
                if len(processed_files) == 1:
                    # Single file download
                    filename, excel_bytes = processed_files[0]
                    clean_filename = Path(filename).stem + "_processed.xlsx"
                    
                    st.download_button(
                        label=f"📊 Download {clean_filename}",
                        data=excel_bytes,
                        file_name=clean_filename,
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    # Multiple files - create ZIP
                    zip_bytes = create_zip_file(processed_files)
                    
                    if zip_bytes is not None:
                        st.download_button(
                            label=f"📦 Download All Files as ZIP ({len(processed_files)} files)",
                            data=zip_bytes,
                            file_name="processed_excel_files.zip",
                            mime="application/zip"
                        )
                        
                        # Also show individual file download options
                        st.markdown("**Or download individual files:**")
                        for filename, excel_bytes in processed_files:
                            clean_filename = Path(filename).stem + "_processed.xlsx"
                            st.download_button(
                                label=f"📊 {clean_filename}",
                                data=excel_bytes,
                                file_name=clean_filename,
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                key=f"download_{filename}"
                            )
            else:
                st.markdown('<div class="error-message">', unsafe_allow_html=True)
                st.markdown("❌ **No files were successfully processed.** Please check your files and try again.")
                st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # Show welcome message when no files are uploaded
        st.markdown("""
        ### 🎯 Welcome to Excel Row Processor!
        
        This tool helps you process Excel files by removing specific rows:
        
        - **Preserves the header row** (first row)
        - **Bulk processing** of multiple files
        - **Flexible options** to delete odd or even rows
        - **Automatic ZIP download** for multiple files
        
        **Supported formats**: .xlsx, .xls
        
        **Maximum file size**: 50MB per file (configurable in sidebar)
        **Maximum files**: 100 files per batch (configurable in sidebar)
        """)
        
        # Example section
        st.markdown("### 📝 Example")
        st.markdown("""
        If you have an Excel file with 10 rows:
        - **Original**: Rows 1-10 (Row 1 is header)
        - **Delete Odd**: Keep rows 1, 3, 5, 7, 9 (header + odd data rows)
        - **Delete Even**: Keep rows 1, 2, 4, 6, 8, 10 (header + even data rows)
        """)

if __name__ == "__main__":
    main()
