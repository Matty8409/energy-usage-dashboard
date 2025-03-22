import pandas as pd
import openpyxl
import glob
import os
from dash import Dash, html, dash_table

app = Dash()

path = 'CSV_files'
all_files = glob.glob(os.path.join(path, '**', '*.xlsx'), recursive=True)

data_by_date = {}

for filename in all_files:
    df = pd.read_excel(filename, index_col=None, header=0)
    date_key = os.path.basename(os.path.dirname(filename))

    if date_key not in data_by_date:
        data_by_date[date_key] = []

    # Append the data frame to the list for this date
    data_by_date[date_key].append(df)

combined_data = []
for date, dfs in data_by_date.items():
    for df in dfs:
        df['Date'] = date  # Add a column with the date for easy reference
        combined_data.append(df)

# Concatenate all the data into one dataframe
df_combined = pd.concat(combined_data, ignore_index=True)

# Initialize the app layout
app.layout = [
    html.Div(children='Energy Usage Dashboard'),
    dash_table.DataTable(
        data=df_combined.to_dict('records'),  # Convert the dataframe to a dictionary
        page_size=10,  # Number of rows per page
        style_table={'height': '300px', 'overflowY': 'auto'},  # Table with scroll
        style_cell={'textAlign': 'center'}  # Center align the text in the cells
    )
]

if __name__ == '__main__':
    app.run(debug=True)









# example of how i will access data
date_to_access = '2025-03-21'

if date_to_access in data_by_date:
    # Print out data from the first file in the list for the given date
    print(f"Data for {date_to_access}:")
    print(data_by_date[date_to_access][3])  # Print the first 5 rows of the first file
else:
    print(f"No data found for {date_to_access}")

# it's a dictionary where the key is the date to access and the value is a list with each entry as the data