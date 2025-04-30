# Energy Usage Dashboard
https://tinyurl.com/22xkubs4

A web-based dashboard for visualizing and analyzing energy usage data. This application allows users to upload energy data files, view data in various formats (table, line graph, heatmap), and perform statistical analysis.

## Features

- **User Authentication**: Login and registration functionality.
- **Data Upload**: Upload CSV or ZIP files containing energy usage data.
- **Data Visualization**:
  - Table view
  - Line graph view
  - Heatmap view
- **Date Filtering**: Select specific dates or view averages.
- **Energy Type Filtering**: Filter data by energy type (e.g., electricity, gas, water).
- **Statistics**: Analyze energy usage trends and patterns.

## Technologies Used

- **Backend**: Flask
- **Frontend**: Dash, Dash Bootstrap Components
- **Database**: SQLAlchemy (SQLite/PostgreSQL)
- **Data Processing**: Pandas
- **Visualization**: Plotly

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Matty8409/energy-usage-dashboard
   cd energy-usage-dashboard
    ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv\Scripts\activate  # On mac: venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the application:
   ```bash
   python run.py
   ```

6. Access the app in your browser at `http://127.0.0.1:8050`.

## Usage

1. **Login/Register**: Create an account or log in to access the dashboard.
2. **Upload Data**: Use the "Upload File or ZIP Folder" button to upload energy data files.
3. **View Data**: Switch between table, line graph, and heatmap views using the radio buttons.
4. **Filter Data**: Use the dropdowns to filter by date or energy type.
5. **Analyze Statistics**: Navigate to the statistics page for detailed analysis.

## File Structure

```
app/
├── __init__.py                 # Initialize the Flask app
├── app.py                      # Main application file
├── auth.py                     # User authentication functions
├── config.py                   # Configuration settings
├── data_processing.py          # Data processing logic
├── database.py                 # Database models and initialization
├── layouts.py                  # Layout definitions for different pages
├── login.py                    # Login and authentication logic
├── models.py                   # View functions for different routes
├── register.py                 # Registration logic
├── routes.py                   # Route definitions for different pages
├── run.py                      # Entry point to run the app
├── save_data_collection.py     # Data collection and saving logic
├── statistics.py               # Statistical analysis functions
├── assets/                     # Static assets (CSS, images, etc.)
```

## Deployment

1. Install Gunicorn:
   ```bash
   pip install gunicorn
   ```

2. Deploy using the `Procfile`:
   ```bash
   web: gunicorn run:server
   ```

3. Set environment variables for production (e.g., `DATABASE_URL`, `SECRET_KEY`).

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes and push the branch.
4. Submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Acknowledgments

- [Dash](https://dash.plotly.com/)
- [Flask](https://flask.palletsprojects.com/)
- [Plotly](https://plotly.com/)
