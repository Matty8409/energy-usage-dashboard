import zipfile
import pandas as pd
import base64
import pytest
import sys
import os
from unittest.mock import patch
from app.data_processing import apply_pulse_ratios, process_uploaded_file, load_initial_csv_data
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#Tests for the apply_pulse_ratios function.

def test_apply_pulse_ratios():
    # Sample input DataFrame
    data = {
        'TH-E-01 kWh (kWh) [DELTA] 1': [10, 20, 30],
        'TH-PM-01.TH-G-01 kWh (kWh) [DELTA] 1': [100, 200, 300],
        'Other Column': [1, 2, 3]
    }
    df = pd.DataFrame(data)

    # Sample pulse_ratios
    pulse_ratios = {
        'TH-E-01 kWh (kWh) [DELTA] 1': 1,
        'TH-PM-01.TH-G-01 kWh (kWh) [DELTA] 1': 0.1
    }

    # Expected output DataFrame
    expected_data = {
        'TH-E-01 kWh (kWh) [DELTA] 1': [10, 20, 30],
        'TH-PM-01.TH-G-01 kWh (kWh) [DELTA] 1': [10.0, 20.0, 30.0],
        'Other Column': [1, 2, 3]
    }
    expected_df = pd.DataFrame(expected_data)

    # Apply the function
    result_df = apply_pulse_ratios(df, pulse_ratios)

    # Assert the result matches the expected output
    pd.testing.assert_frame_equal(result_df, expected_df)

# Test when pulse_ratios contains keys not in the DataFrame
def test_apply_pulse_ratios_missing_columns():
    data = {
        'TH-E-01 kWh (kWh) [DELTA] 1': [10, 20, 30],
        'Other Column': [1, 2, 3]
    }
    df = pd.DataFrame(data)

    pulse_ratios = {
        'TH-E-01 kWh (kWh) [DELTA] 1': 1,
        'Nonexistent Column': 0.5
    }

    expected_data = {
        'TH-E-01 kWh (kWh) [DELTA] 1': [10, 20, 30],
        'Other Column': [1, 2, 3]
    }
    expected_df = pd.DataFrame(expected_data)

    result_df = apply_pulse_ratios(df, pulse_ratios)
    pd.testing.assert_frame_equal(result_df, expected_df)

# Test with an empty DataFrame
def test_apply_pulse_ratios_empty_dataframe():
    df = pd.DataFrame()
    pulse_ratios = {'TH-E-01 kWh (kWh) [DELTA] 1': 1}

    expected_df = pd.DataFrame()
    result_df = apply_pulse_ratios(df, pulse_ratios)
    pd.testing.assert_frame_equal(result_df, expected_df)

# Test when no columns match
def test_apply_pulse_ratios_no_matching_columns():
    data = {
        'Other Column': [1, 2, 3]
    }
    df = pd.DataFrame(data)

    pulse_ratios = {
        'Nonexistent Column': 0.5
    }

    expected_df = pd.DataFrame(data)
    result_df = apply_pulse_ratios(df, pulse_ratios)
    pd.testing.assert_frame_equal(result_df, expected_df)

#Tests for process_uploaded_file function.

def test_process_uploaded_file_valid_zip(tmpdir):
    # Create a temporary ZIP file with an Excel file
    zip_path = tmpdir.join("test.zip")
    excel_path = tmpdir.join("test.xlsx")
    df = pd.DataFrame({'A': [1, 2], 'B': [3, 4], 'Time': ['12:00', '13:00']})  # Add 'Time' column
    df.to_excel(excel_path, index=False, engine='openpyxl')

    with zipfile.ZipFile(zip_path, 'w') as z:
        z.write(excel_path, arcname="test.xlsx")

    # Encode the ZIP file as base64
    with open(zip_path, 'rb') as f:
        encoded_zip = base64.b64encode(f.read()).decode('utf-8')

    # Mock the UPLOAD_FOLDER to use the temporary directory
    with patch('app.data_processing.UPLOAD_FOLDER', str(tmpdir)):
        contents = f"data:application/zip;base64,{encoded_zip}"
        filename = "uploaded_test.zip"
        result = process_uploaded_file(contents, filename, None)

    # Assert the result
    assert isinstance(result, list)
    assert len(result) > 0

# Test for process_uploaded_file with an invalid file
def test_process_uploaded_file_invalid_file(tmpdir):
    contents = "data:text/plain;base64,SGVsbG8gd29ybGQ="  # Base64 for "Hello world"
    filename = "invalid_test.txt"  # Use a unique file name

    # Mock the UPLOAD_FOLDER to use the temporary directory
    with patch('app.data_processing.UPLOAD_FOLDER', str(tmpdir)):
        with pytest.raises(ValueError, match="Only ZIP files are supported for this operation."):
            process_uploaded_file(contents, filename, None)

def test_process_uploaded_file_multiple_excel_files(tmpdir):
    zip_path = tmpdir.join("test.zip")
    excel_path1 = tmpdir.join("test1.xlsx")
    excel_path2 = tmpdir.join("test2.xlsx")
    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4], 'Time': ['12:00', '13:00']})
    df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8], 'Time': ['14:00', '15:00']})
    df1.to_excel(excel_path1, index=False, engine='openpyxl')
    df2.to_excel(excel_path2, index=False, engine='openpyxl')

    with zipfile.ZipFile(zip_path, 'w') as z:
        z.write(excel_path1, arcname="test1.xlsx")
        z.write(excel_path2, arcname="test2.xlsx")

    with open(zip_path, 'rb') as f:
        encoded_zip = base64.b64encode(f.read()).decode('utf-8')

    with patch('app.data_processing.UPLOAD_FOLDER', str(tmpdir)):
        contents = f"data:application/zip;base64,{encoded_zip}"
        filename = "uploaded_test.zip"
        result = process_uploaded_file(contents, filename, None)

    assert isinstance(result, list)
    assert len(result) > 0

# Test for process_uploaded_file with no Excel files in ZIP
def test_process_uploaded_file_no_excel_files(tmpdir):
    zip_path = tmpdir.join("test.zip")
    text_file = tmpdir.join("test.txt")
    text_file.write("This is a test file.")

    with zipfile.ZipFile(zip_path, 'w') as z:
        z.write(text_file, arcname="test.txt")

    with open(zip_path, 'rb') as f:
        encoded_zip = base64.b64encode(f.read()).decode('utf-8')

    with patch('app.data_processing.UPLOAD_FOLDER', str(tmpdir)):
        contents = f"data:application/zip;base64,{encoded_zip}"
        filename = "uploaded_test.zip"
        with pytest.raises(ValueError, match="Only ZIP files are supported for this operation."):
            process_uploaded_file(contents, filename, None)

# Test for load_initial_csv_data with multiple Excel files
def test_load_initial_csv_data_multiple_files(tmpdir):
    excel_path1 = tmpdir.join("test1.xlsx")
    excel_path2 = tmpdir.join("test2.xlsx")
    df1 = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})
    df2 = pd.DataFrame({'A': [5, 6], 'B': [7, 8]})
    df1.to_excel(excel_path1, index=False, engine='openpyxl')
    df2.to_excel(excel_path2, index=False, engine='openpyxl')

    result = load_initial_csv_data(path=str(tmpdir))
    assert not result.empty
    assert len(result) == 4

# Test for load_initial_csv_data with multiple files
def test_load_initial_csv_data_empty_directory(tmpdir):
    # Ensure the temporary directory is empty
    assert len(os.listdir(tmpdir)) == 0

    # Call the function with the temporary directory path
    result = load_initial_csv_data(path=str(tmpdir))

    # Assert the result is an empty DataFrame
    assert result.empty