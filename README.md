# Stocks Data Management Web App

This is a Flask-based web application for fetching, processing, and downloading financial data for S&P 500 companies. The data is retrieved, processed into a CSV file, and made available for download. The application also includes a progress bar to monitor the update process.

## Features
- Fetches financial data for S&P 500 companies.
- Saves data as a CSV file.
- Provides a downloadable link for the latest data.
- Displays the last update timestamp and time since last update.
- Includes a progress bar for real-time update tracking.

## Installation and Setup

1. Clone the repository:
   ```sh
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Run the application:
   If running on your local machine, add the following lines to `app.py` before executing it:
   ```python
   if __name__ == '__main__':
       app.run(debug=True)
   ```
   Then start the server:
   ```sh
   python app.py
   ```
   If using PythonAnywhere, these lines should **not** be included, as the application will be managed by the PythonAnywhere web service.

4. Open the app in your browser:
   ```
   http://127.0.0.1:5000
   ```

## Usage

- Click the **Update Data** button to start fetching new financial data.
- A progress bar will appear to indicate update progress.
- Once completed, a **Download CSV** button will be available to download the latest dataset.

### ⚠ Warning
The update process can take **up to 3 hours** to complete. Please be patient while the data is being fetched.

## File Overview

### `app.py`
This file contains the Flask application, structured using a `DataUpdater` class to manage the update process, handle progress tracking, and serve the web interface.

### `main.py`
Contains core data processing functions:
- `get_symbols()`: Fetches S&P 500 tickers.
- `get_financial_data(symbol, metrics)`: Retrieves financial metrics for a given symbol.
- `get_last_updated_time(folder_path)`: Checks the last update time of CSV reports.
- `delete_previous(folder_path)`: Deletes previous reports before saving new ones.
- `save_csv(df, outputs_path)`: Saves financial data as a CSV file.
- `get_data()`: Fetches and processes data for multiple S&P 500 companies.

### `templates/index.html`
The front-end interface using HTML and JavaScript to display update progress, provide a download link, and initiate data updates.

## Deployment on PythonAnywhere

To deploy this app on PythonAnywhere:
1. Upload the project files to PythonAnywhere.
2. Set up a Flask web app and configure the WSGI entry point.
3. Ensure dependencies are installed using `pip install --user -r requirements.txt`.
4. The web app will be managed by PythonAnywhere and should not include `if __name__ == '__main__':` in `app.py`.

## License
This project is open-source and available under the Apache-2.0 License.

