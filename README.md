# System Analysis Configurations Dashboard

## Overview
This web application is designed to aggregate all the information needed to start automated tests using Jenkins.

Users can view and manage device and network configurations before kicking off new builds on Jenkins.

## Hosting
This application is hosted on Render, a free online hosting tool.

This can be accessed at https://system-analysis-dashboard.onrender.com

## CI/CD
This application has two continuous integration pipelines built using GitHub Actions.

* The PR pipeline will run whenever a new pull request is opened, and runs the Black, Pylint, Integration Tests and Security Tests pipelines.

    * These will check the formatting and style of the incoming code, as well as that the tests pass.

* The Merge pipeline runs whenever a pull request is closed, and automatically deploys the web application on Render.

## Setup
To run the application locally, follow these steps:

1. Navigate to the `web-app-assignment/` directory in a terminal
2. Install the requirements for this application
    ```commandline
    pip install -r requirements.txt
    ```
3. Set the environment variables

    Windows:
    ```commandline
    set DATABASE_URL={database url}
    set SECRET_KEY={secret key}
    ```
    MacOS/Linux:
    ```commandline
    export DATABASE_URL={database url}
    export SECRET_KEY={secret key}
    ```
4. Set the flask application environment variable

    Windows:
    ```commandline
    set FLASK_APP=app.py
    ```
    MacOS/Linux:
    ```commandline
    export FLASK_APP=app.py
    ```
    
    
5. Set up the database migrations directory
    ```commandline
    flask db init
    flask db migrate -m "<your message here>"
    flask db upgrade
    ```

6. Run the setup file to populate the database with example data
    ```commandline
    python populate_database.py
    ```
Note: While the web application can be run without populating the database tables, the only way to add an administrator account is through this script.
It's recommended to run the full setup script.
## Running the application

1. Run `app.py` to launch the dashboard
    ```commandline
    python app.py
    ```
    The dashboard will be hosted on `http://127.0.0.1:5000/`


## Running the tests

The integration tests have been written using the `unittest` python module.

Visual Studio Code has a built-in testing suite that will run the tests.

To configure it, set the test folder to `integration_tests/` and the pattern to look for as `test_*.py`

The security tests can be run in the same way, instead setting the test folder as `security_tests/`.
