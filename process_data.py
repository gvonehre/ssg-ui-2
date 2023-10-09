import pandas as pd
import shutil
import os

def process_and_zip_excel(file, output_zip_path, original_name):
    """
    Process the Excel file and zip the original and processed files.

    Parameters:
        file (BytesIO): The uploaded Excel file.
        output_zip_path (str): The path to save the zipped file.

    Returns:
        str: The path to the zipped file.
    """
    # Load the Excel file into a DataFrame
    df = pd.read_excel(file, engine='openpyxl')

    # [Your Additional Processing Logic Here]
    # For now, let's just create a copy of the original DataFrame
    processed_df = df.copy()

    # Save the original and processed DataFrames to Excel files
    original_file_path = f"{original_name}.xlsx"
    processed_file_path = "processed_file.xlsx"

    with pd.ExcelWriter(original_file_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    with pd.ExcelWriter(processed_file_path, engine='xlsxwriter') as writer:
        processed_df.to_excel(writer, index=False, sheet_name='Sheet1')

    # Ensure the directory for the zip file exists
    os.makedirs(os.path.dirname(output_zip_path), exist_ok=True)

    # Compress the Excel files into a .zip file
    shutil.make_archive(output_zip_path, 'zip', '.', '.')

    # Clean up the original Excel files
    os.remove(original_file_path)
    os.remove(processed_file_path)

    return f"{output_zip_path}.zip"