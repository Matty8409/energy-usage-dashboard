# data_processing.py
import glob
import os
import pandas as pd
import base64
import io
import zipfile
import openpyxl
import logging
from app.config import pulse_ratios, energy_type_mapping

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
                            date_key = os.path.basename(file).split('_')[0] if '_' in file else 'Unknown'
                            folder_path = os.path.join(UPLOAD_FOLDER, date_key)
                            os.makedirs(folder_path, exist_ok=True)
                            save_path = os.path.join(folder_path, file)
                            with open(save_path, 'wb') as out_file:
                                out_file.write(f.read())

                            # Process the extracted .xlsx file
                            df_new = pd.read_excel(save_path, engine='openpyxl')
                            df_new['Date'] = pd.to_datetime(date_key)
                            if existing_data is None:
                                existing_data = df_new
                            else:
                                existing_data = pd.concat([pd.DataFrame(existing_data), df_new], ignore_index=True)

            # Ensure sorting and grouping after processing all files
            if 'Date' in existing_data.columns and 'Time' in existing_data.columns:
                existing_data = existing_data.sort_values(by=['Date', 'Time'])
                existing_data = existing_data.groupby(['Date', 'Time'], as_index=False).first()

            return existing_data

        else:
            date_key = os.path.basename(filename).split('_')[0] if '_' in filename else 'Unknown'
            folder_path = os.path.join(UPLOAD_FOLDER, date_key)
            os.makedirs(folder_path, exist_ok=True)
            save_path = os.path.join(folder_path, filename)
            with open(save_path, 'wb') as out_file:
                out_file.write(decoded)

            if filename.endswith('.xlsx'):
                df_new = pd.read_excel(io.BytesIO(decoded), engine='openpyxl')
                df_new['Date'] = pd.to_datetime(date_key)
                if existing_data is None:
                    existing_data = df_new
                else:
                    existing_data = pd.concat([pd.DataFrame(existing_data), df_new], ignore_index=True)

                if 'Date' in existing_data.columns and 'Time' in existing_data.columns:
                    existing_data = existing_data.sort_values(by=['Date', 'Time'])
                    existing_data = existing_data.groupby(['Date', 'Time'], as_index=False).first()

                return existing_data

        return existing_data

    except Exception as e:
        logging.error(f"Error processing file {filename}: {e}")
        raise

def load_initial_csv_data(path=UPLOAD_FOLDER):
    logging.debug(f"Loading data from {path}")
    all_files = glob.glob(os.path.join(path, '**', '*.xlsx'), recursive=True)
    combined_data = []
    for filename in all_files:
        try:
            # Read the Excel file
            df = pd.read_excel(filename, engine='openpyxl')

            # Ensure the `Date` column is in the correct format
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date']).dt.date  # Keep only the date part

            combined_data.append(df)
        except Exception as e:
            logging.error(f"Error processing file {filename}: {e}")

    if not combined_data:
        logging.error("No files found in the upload folder.")
        return pd.DataFrame()

    # Combine all data into a single DataFrame
    df_combined = pd.concat(combined_data, ignore_index=True)

    # Ensure sorting and grouping by `Date` and `Time` if both columns exist
    if 'Date' in df_combined.columns and 'Time' in df_combined.columns:
        df_combined = df_combined.sort_values(by=['Date', 'Time'])
        df_combined = df_combined.groupby(['Date', 'Time'], as_index=False).first()

    return df_combined

def apply_pulse_ratios(df, pulse_ratios):
    for column, ratio in pulse_ratios.items():
        if column in df.columns:
            df[column] = (df[column] * ratio).round(3)
    return df

def get_processed_data():
    df = load_initial_csv_data()
    df = apply_pulse_ratios(df, pulse_ratios)
    return df

def convert_gas_to_kwh(df):
    gas_column = next((col for col, energy_type in energy_type_mapping.items() if energy_type == 'Gas'), None)
    if gas_column and gas_column in df.columns:
        gas_conversion_factor = 11.2  # Example: 1 m³ of gas = 11.2 kWh
        df[gas_column] = df[gas_column] * gas_conversion_factor
    return df