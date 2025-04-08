# dataProcessing.py
import glob
import os
import pandas as pd
import base64
import io
import zipfile
import openpyxl
from config import pulse_ratios

UPLOAD_FOLDER = r'C:\Users\mattm\Documents\GitHub\finalProjectTesting\CSV_files'  # Directory to save uploaded files
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def process_uploaded_file(contents, filename, existing_data):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    # Extract the date from the file name
    date_key = filename.split('_')[0]  # Assuming the date is the first part of the filename
    target_folder = os.path.join(UPLOAD_FOLDER, date_key)
    os.makedirs(target_folder, exist_ok=True)  # Create the folder for extracted files

    # Save the uploaded ZIP file
    zip_file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(zip_file_path, 'wb') as f:
        f.write(decoded)

    if filename.endswith('.zip'):
        # Unzip the contents into the target folder
        with zipfile.ZipFile(zip_file_path, 'r') as z:
            z.extractall(target_folder)

        # Remove the ZIP file after extraction
        os.remove(zip_file_path)

        # Delete any excess files in the UPLOAD_FOLDER
        for file in os.listdir(UPLOAD_FOLDER):
            file_path = os.path.join(UPLOAD_FOLDER, file)
            if file_path != target_folder and os.path.isfile(file_path):
                os.remove(file_path)

        # Process all extracted files
        df_list = []
        for file in os.listdir(target_folder):
            if file.endswith('.xlsx'):
                file_path = os.path.join(target_folder, file)
                df_new = pd.read_excel(file_path, engine='openpyxl')
                df_new['Date'] = date_key
                df_new = apply_pulse_ratios(df_new, pulse_ratios)
                df_list.append(df_new)

        if existing_data is None:
            df_combined = pd.concat(df_list, ignore_index=True)
        else:
            df_combined = pd.DataFrame(existing_data)
            df_combined = pd.concat([df_combined] + df_list, ignore_index=True)
    else:
        raise ValueError("Only ZIP files are supported for this operation.")

    # Sort and group the combined DataFrame
    df_combined = df_combined.sort_values(by=['Date', 'Time'])
    df_combined = df_combined.groupby(['Date', 'Time'], as_index=False).first()

    return df_combined.to_dict('records')

def load_initial_csv_data(path=r'C:\Users\mattm\Documents\GitHub\finalProjectTesting\CSV_files'):
    all_files = glob.glob(os.path.join(path, '**', '*.xlsx'), recursive=True)
    combined_data = []
    for filename in all_files:
        date_key = os.path.basename(filename).split('_')[0]
        df = pd.read_excel(filename, engine='openpyxl')
        df['Date'] = date_key
        combined_data.append(df)
    df_combined = pd.concat(combined_data, ignore_index=True)
    df_combined = df_combined.sort_values(by=['Date', 'Time'])
    df_combined = df_combined.groupby(['Date', 'Time'], as_index=False).first()
    return df_combined

def apply_pulse_ratios(df, pulse_ratios):
    for column, ratio in pulse_ratios.items():
        if column in df.columns:
            df[column] = df[column] * ratio
    return df