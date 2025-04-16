# data_processing.py
import glob
import os
import pandas as pd
import base64
import io
import zipfile
import openpyxl
import logging

# Dynamically construct the path to the CSV_files folder
BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # Get the project root directory
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'CSV_files')  # Path to the CSV_files folder
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def process_uploaded_file(contents, filename, existing_data):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    try:
        if filename.endswith('.zip'):
            zip_file = io.BytesIO(decoded)
            with zipfile.ZipFile(zip_file, 'r') as z:
                for file in z.namelist():
                    if file.endswith('.xlsx'):
                        with z.open(file) as f:
                            # Extract date key or use a default folder
                            date_key = os.path.basename(file).split('_')[0] if '_' in file else 'Unknown'
                            folder_path = os.path.join(UPLOAD_FOLDER, date_key)
                            os.makedirs(folder_path, exist_ok=True)

                            # Save the extracted file to the correct folder
                            save_path = os.path.join(folder_path, file)
                            with open(save_path, 'wb') as out_file:
                                out_file.write(f.read())
        else:
            # Extract date key or use a default folder
            date_key = os.path.basename(filename).split('_')[0] if '_' in filename else 'Unknown'
            folder_path = os.path.join(UPLOAD_FOLDER, date_key)
            os.makedirs(folder_path, exist_ok=True)

            # Save the uploaded Excel file to the correct folder
            save_path = os.path.join(folder_path, filename)
            with open(save_path, 'wb') as out_file:
                out_file.write(decoded)

        # Process the file and update the data
        if filename.endswith('.xlsx'):
            df_new = pd.read_excel(io.BytesIO(decoded), engine='openpyxl')
            date_key = os.path.basename(filename).split('_')[0] if '_' in filename else 'Unknown'
            df_new['Date'] = date_key
            if existing_data is None:
                df_combined = df_new
            else:
                df_combined = pd.DataFrame(existing_data)
                df_combined = pd.concat([df_combined, df_new], ignore_index=True)

            # Sort and remove duplicates
            if 'Date' in df_combined.columns and 'Time' in df_combined.columns:
                df_combined = df_combined.sort_values(by=['Date', 'Time'])
                df_combined = df_combined.groupby(['Date', 'Time'], as_index=False).first()

            return df_combined.to_dict('records')

        return existing_data

    except Exception as e:
        logging.error(f"Error processing file {filename}: {e}")
        raise

def load_initial_csv_data(path=UPLOAD_FOLDER):
    all_files = glob.glob(os.path.join(path, '**', '*.xlsx'), recursive=True)
    combined_data = []
    for filename in all_files:
        date_key = os.path.basename(filename).split('_')[0]
        df = pd.read_excel(filename, engine='openpyxl')
        df['Date'] = date_key
        combined_data.append(df)

    if not combined_data:  # Return an empty DataFrame if no files are found
        return pd.DataFrame()

    df_combined = pd.concat(combined_data, ignore_index=True)
    df_combined = df_combined.sort_values(by=['Date', 'Time'])
    df_combined = df_combined.groupby(['Date', 'Time'], as_index=False).first()
    return df_combined

def apply_pulse_ratios(df, pulse_ratios):
    for column, ratio in pulse_ratios.items():
        if column in df.columns:
            df[column] = df[column] * ratio
    return df