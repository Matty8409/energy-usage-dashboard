# Energy Usage Dashboard

A web-based dashboard for visualizing and analyzing energy usage data. This application allows users to upload energy data files, view data in various formats (table, line graph, heatmap), and perform statistical analysis.

## Prerequisites
This guide will help you set up and run the Energy Usage Dashboard on your local machine. Before starting, ensure you have the following installed:


**Python**: Download and install Python from python.org. Make sure to add Python to your system PATH during installation.

To verify, run:
```bash
python --version
```

**Git**: Download and install Git from git-scm.com. This is required to clone the repository.

To verify, run:
```bash
git --version
```
## Installation Guide

**1. Clone the repository:**
   
This step downloads the project files to your computer.

Alternative: You can also download the repository as a ZIP file from GitHub and extract it
   ```bash
   git clone https://github.com/Matty8409/energy-usage-dashboard
   cd energy-usage-dashboard
   ```
If system can not find energy-usage-dashboard use full path ie C:\Users\Sam\Desktop\Python DEV\energy-usage-dashboard

**2. Create a virtual environment:**
   
A virtual environment isolates the project dependencies from your system Python installation.

Alternative: You can use tools like conda or pipenv instead of venv.
   ```bash
   python -m venv venv
   ```

**3. Activate the virtual environment**
   
On windows
   ```bash
   venv/bin/activate
   ```
On mac
   ```bash
   source venv\Scripts\activate
   ```
4. Install dependencies:

This step installs all the required Python libraries listed in the requirements.txt file.

Alternative: If you encounter issues, try installing dependencies manually through IDE.


   ```bash
   pip install -r requirements.txt
   ```


5. Run the application:

This command starts the Flask server and Dash application.

Alternative: You can use an IDE like PyCharm to run the run.py file directly.

   ```bash
   python run.py
   ```

6. Access the app in your browser at `http://127.0.0.1:8050`.

### Heroku Deployment

The application is deployed on Heroku and can be accessed at:

https://tinyurl.com/22xkubs4

#### Important Notes:
-It is recommended to run the application on your local system for better performance and full functionality.

-Some features may be limited on Heroku due to incomplete database integration.

-The app runs slower on Heroku due to the limitations of the free (Eco) plan.

-This deployment is temporary and may not remain available indefinitely.


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
