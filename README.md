# System Analysis Configurations Dashboard

## Overview
This web application is designed to aggregate all the information needed to start automated tests using Jenkins

Users can view and manage device and network configurations before kicking off new builds on Jenkins.

## Setup
1. Navigate to the `web-app-assignment/` directory in a terminal
2. Install the requirements for this application
    ```commandline
    pip install -r requirements.txt
    ```
3. Set the flask application environment variable

    Windows:
    ```commandline
    set FLASK_APP=app.py
    ```
    MacOS/Linux:
    ```commandline
    export FLASK_APP=app.py
    ```
    
    
4. Set up the database migrations directory
    ```commandline
    flask db init
    flask db migrate -m "<your message here>"
    flask db upgrade
    ```

5. Run the setup file to populate the database with example data
    ```commandline
    python database_setup.py
    ```

## Running the application

1. Run `app.py` to launch the dashboard
    ```commandline
    python app.py
    ```
    The dashboard will be hosted on `http://127.0.0.1:5000/`