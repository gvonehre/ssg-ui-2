import streamlit as st
import pandas as pd
import io
import base64
from process_data import process_and_zip_excel  # Import the processing function

def get_binary_file_downloader_html(bin_file, file_label='File'):
    bin_file.seek(0)
    b64 = base64.b64encode(bin_file.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_label}">Download {file_label}</a>'
    return href

st.title("Excel Processor")
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")

if uploaded_file:
    original_name = uploaded_file.name.rsplit(".", 1)[0]

    if st.button("Process File"):
        # Specify the path for the zip file
        output_zip_path = "processed_files/processed_files"  # 'processed_files' directory

        # Process the Excel file and zip the original and processed files
        output_zip_path = process_and_zip_excel(uploaded_file, output_zip_path, original_name)

        # Provide a download link for the .zip file
        with open(output_zip_path, "rb") as f:
            st.markdown(get_binary_file_downloader_html(f, 'processed_files.zip'), unsafe_allow_html=True)
