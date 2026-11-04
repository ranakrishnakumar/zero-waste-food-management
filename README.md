# Zero Waste Food Management App

A beginner-friendly Flask + SQLite project for listing surplus food, requesting donations, and updating collection status.

## Requirements
- Python 3.10 or newer
- VS Code or GitHub Codespaces
- Internet connection for Bootstrap styling (optional; app functionality is local)

## Run on Windows
1. Extract the ZIP file.
2. Open the `zero_waste_food_app` folder in VS Code.
3. Open Terminal > New Terminal.
4. Create a virtual environment:
   `py -m venv venv`
5. Activate it:
   PowerShell: `venv\Scripts\Activate.ps1`
   Command Prompt: `venv\Scripts\activate.bat`
6. Install dependencies:
   `python -m pip install -r requirements.txt`
7. Start the application:
   `python app.py`
8. Open this address in Chrome/Edge:
   `http://127.0.0.1:5000`

## Run in GitHub Codespaces
1. Upload/extract the project into your repository and open it in Codespaces.
2. In the terminal run:
   `python -m pip install -r requirements.txt`
3. Run:
   `python app.py`
4. Open the Ports tab, find port `5000`, and select **Open in Browser**.

The SQLite database `zero_waste.db` is created automatically on first run.

## Test the app
1. Select **Donate Food** and add a sample donation.
2. Return to the home page and confirm it appears.
3. Enter an NGO/requester name and select **Request food**.
4. Select **Mark as collected** to complete the workflow.

## Important
This is an academic demonstration, not a production food-safety platform. Before real deployment, add user authentication, role-based permissions, input validation, secure configuration, privacy protections, and food-safety/expiry verification. The demo currently allows anyone who can access the page to update collection status or delete records is not exposed in the UI.