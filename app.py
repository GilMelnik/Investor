import os
import threading
import logging
from time import sleep
from datetime import datetime

import pandas as pd
from flask import Flask, render_template, send_file, jsonify
from main import save_csv, get_symbols, get_financial_data, get_last_updated_time

app = Flask(__name__)
OUTPUTS_PATH = "/home/melniknoob/Investor/static/reports/"
PROGRESS = 0
IS_UPDATING = False
LAST_UPDATED = None  # To store the last update timestamp
logging.basicConfig(filename='/home/melniknoob/Investor/logfile.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filemode='w')
logger = logging.getLogger("app_log")
logger.setLevel(logging.DEBUG)


def get_data():
    global PROGRESS, IS_UPDATING, LAST_UPDATED, logger
    logger.debug("starting get_data")
    IS_UPDATING = True  # Mark as updating
    PROGRESS = 0  # Reset progress

    # Fetch data for all S&P 500 companies
    sp500_tickers = get_symbols()[:5]
    logger.debug("got sp500 symbols")
    metrics = [
        'enterpriseValue',
        'marketCap',
        'beta',
        'debtToEquity',
        'returnOnEquity',
        "trailingPE",
        "enterpriseToEbitda",
        "totalRevenue",
        "revenueGrowth",
        "debtToEquity",
        "operatingCashflow",
    ]
    data = dict()
    logger.debug("starting main loop")
    for i, symbol in enumerate(sp500_tickers):
        logger.debug(f"calling symbol num {i}: {symbol}")
        data[symbol] = get_financial_data(symbol, metrics)
        PROGRESS = int(((i + 1) / len(sp500_tickers)) * 100)  # Update progress percentage
        sleep(3)

    # Convert to DataFrame and save to CSV
    df = pd.DataFrame.from_dict(data, orient="index")
    save_csv(df, OUTPUTS_PATH)

    LAST_UPDATED = datetime.now()  # Update the last updated time
    PROGRESS = 100  # Mark progress as complete
    IS_UPDATING = False  # Mark as not updating anymore


@app.route('/')
def index():
    global LAST_UPDATED, PROGRESS, IS_UPDATING
    latest_file, last_updated_time = get_last_updated_time(OUTPUTS_PATH)
    if not last_updated_time:
        return render_template(
            'index.html',
            last_updated="Never",
            time_since_update="N/A",
            download_filename=None,
            is_updating=IS_UPDATING,
            progress=PROGRESS,
        )
    if not LAST_UPDATED:
        LAST_UPDATED = last_updated_time

    time_since_update = datetime.now() - last_updated_time

    return render_template(
        'index.html',
        last_updated=last_updated_time.strftime("%Y-%m-%d %H:%M:%S"),
        time_since_update=str(time_since_update).split('.')[0],  # Remove microseconds
        download_filename=latest_file,
        is_updating=IS_UPDATING,
        progress=PROGRESS,
    )


@app.route('/download/<filename>')
def download(filename):
    file_path = os.path.join(OUTPUTS_PATH, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404



@app.route('/start-update', methods=['POST'])
def start_update():
    global IS_UPDATING
    if not IS_UPDATING:  # Only allow one update at a time
        threading.Thread(target=get_data).start()  # Run `get_data` in a separate thread
        return jsonify({"status": "Update started"})
    else:
        return jsonify({"status": "Update already in progress"}), 400


@app.route('/progress')
def progress():
    global PROGRESS, IS_UPDATING
    return jsonify({"progress": PROGRESS, "is_updating": IS_UPDATING})
