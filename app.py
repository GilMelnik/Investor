import os
import threading
import logging
from time import sleep
from datetime import datetime

import pandas as pd
from flask import Flask, render_template, send_file, jsonify
from main import save_csv, get_symbols, get_financial_data, get_last_updated_time


class DataUpdater:
    def __init__(self, output_path, log_file):
        self.app = Flask(__name__)
        self.output_path = output_path
        self.progress = 0
        self.is_updating = False
        self.last_updated = None

        logging.basicConfig(
            filename=log_file,
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filemode='w'
        )
        self.logger = logging.getLogger("app_log")
        self.logger.setLevel(logging.DEBUG)

        self._setup_routes()

    def _setup_routes(self):
        self.app.add_url_rule('/', 'index', self.index)
        self.app.add_url_rule('/download/<filename>', 'download', self.download)
        self.app.add_url_rule('/start-update', 'start_update', self.start_update, methods=['POST'])
        self.app.add_url_rule('/progress', 'progress', self.progress_status)

    def get_data(self):
        self.logger.debug("Starting data update")
        self.is_updating = True
        self.progress = 0

        sp500_tickers = get_symbols()
        self.logger.debug("Got S&P 500 symbols")
        metrics = [
            'enterpriseValue', 'marketCap', 'beta', 'debtToEquity', 'returnOnEquity',
            "trailingPE", "enterpriseToEbitda", "totalRevenue", "revenueGrowth",
            "debtToEquity", "operatingCashflow"
        ]
        data = {}
        self.logger.debug("Starting data fetch loop")
        for i, symbol in enumerate(sp500_tickers):
            self.logger.debug(f"Fetching data for symbol {i}: {symbol}")
            data[symbol] = get_financial_data(symbol, metrics)
            self.progress = int(((i + 1) / len(sp500_tickers)) * 100)
            sleep(3)

        self.logger.debug("Finished fetching data, saving to csv")
        df = pd.DataFrame.from_dict(data, orient="index")
        save_csv(df, self.output_path)

        self.last_updated = datetime.now()
        self.progress = 100
        self.is_updating = False
        self.logger.debug("Finished updating data")

    def index(self):
        latest_file, last_updated_time = get_last_updated_time(self.output_path)
        if not last_updated_time:
            return render_template(
                'index.html', last_updated="Never", time_since_update="N/A",
                download_filename=None, is_updating=self.is_updating, progress=self.progress
            )
        if not self.last_updated:
            self.last_updated = last_updated_time

        time_since_update = datetime.now() - last_updated_time
        return render_template(
            'index.html', last_updated=last_updated_time.strftime("%Y-%m-%d %H:%M:%S"),
            time_since_update=str(time_since_update).split('.')[0],
            download_filename=latest_file, is_updating=self.is_updating, progress=self.progress
        )

    def download(self, filename):
        file_path = os.path.join(self.output_path, filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        return jsonify({"error": "File not found"}), 404

    def start_update(self):
        if not self.is_updating:
            threading.Thread(target=self.get_data).start()
            return jsonify({"status": "Update started"})
        return jsonify({"status": "Update already in progress"}), 400

    def progress_status(self):
        return jsonify({"progress": self.progress, "is_updating": self.is_updating})


data_updater = DataUpdater(
    "/home/melniknoob/Investor/static/reports/",
    "/home/melniknoob/Investor/logfile.log"
    )
app = data_updater.app
