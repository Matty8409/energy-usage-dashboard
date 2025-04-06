# dataProcessing.py
import glob
import os
import pandas as pd
import base64
import io
import zipfile
import openpyxl

def process_uploaded_file(contents, filename, existing_data):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)

    if filename.endswith('.zip'):
        zip_file = io.BytesIO(decoded)
        with zipfile.ZipFile(zip_file, 'r') as z:
            df_list = []
            for file in z.namelist():
                if file.endswith('.xlsx'):
                    with z.open(file) as f:
                        df_new = pd.read_excel(f, engine='openpyxl')
                        date_key = os.path.basename(file).split('_')[0]
                        df_new['Date'] = date_key
                        df_list.append(df_new)
            if existing_data is None:
                df_combined = pd.concat(df_list, ignore_index=True)
            else:
                df_combined = pd.DataFrame(existing_data)
                df_combined = pd.concat([df_combined] + df_list, ignore_index=True)
    else:
        df_new = pd.read_excel(io.BytesIO(decoded), engine='openpyxl')
        date_key = os.path.basename(filename).split('_')[0]
        df_new['Date'] = date_key
        if existing_data is None:
            df_combined = df_new
        else:
            df_combined = pd.DataFrame(existing_data)
            df_combined = pd.concat([df_combined, df_new], ignore_index=True)

    df_combined = df_combined.sort_values(by=['Date', 'Time'])
    df_combined = df_combined.groupby(['Date', 'Time'], as_index=False).first()

    return df_combined.to_dict('records')

def load_initial_csv_data(path='CSV_files'):
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