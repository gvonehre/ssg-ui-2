import os
import shutil
import streamlit as st
import pandas as pd
import base64
import io


def get_binary_file_downloader_html(bin_file, file_label='File'):
    bin_file.seek(0)
    b64 = base64.b64encode(bin_file.read()).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{file_label}">Download {file_label}</a>'
    return href

def get_download_link(file, filename, text="Download"):
    """
    Generates a link to download the file.
    """
    b64 = base64.b64encode(file.getvalue()).decode()  # Use getvalue() to get bytes
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">{text}</a>'

def get_excel_download_link(df, filename):
    """Generate a link to download the DataFrame as an Excel file"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Sheet1', index=False)
    excel_data = output.getvalue()
    b64 = base64.b64encode(excel_data).decode()  # Encode to base64
    href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{filename}">Download Excel File</a>'
    return href

#Initialize variable
original_name = ""
#specify path for output zip file
output_zip_path = "processed_files/processed_files"

# Choose Excel File
st.title("SSG - Data Enrichment Tool")
upload_excel = st.file_uploader("Choose an Excel file", type="xlsx")

if upload_excel:
    # store Original File Name
    original_name = upload_excel.name.rsplit(".", 1)[0]
    #Define Sublocation
    sublocation = 'ProcessedFiles'


    # If Button pressed
    if st.button("Start processing File"):
        df = pd.read_excel(upload_excel, engine='openpyxl')

        # Define and Create Sublocation
        sublocation = 'temp/ProcessedFiles'
        location = 'temp'
        os.makedirs(sublocation, exist_ok=True)

        # define output file
        output_excel = f"{sublocation}/{original_name}_processed"

        df.to_excel(output_excel, engine='openpyxl')


        #Download Single Excel File
        #st.markdown(get_excel_download_link(df, output_excel), unsafe_allow_html=True)

        #Download Zip Folder
        zip_name = "temp/download.zip"
        if os.path.exists(location):
            shutil.make_archive(zip_name.replace('.zip',''), 'zip', sublocation, )


        with open(zip_name, "rb") as file:
            st.download_button( label="Download Zip Folder", data=file, file_name='archive.zip', mime='application/zip', )
            # remove Files after Download
            os.remove(zip_name)
            os.remove(f"{sublocation}/{original_name}_processed")