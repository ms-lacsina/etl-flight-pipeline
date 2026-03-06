import os
import logging
from fetch_data import fetch_forecast_data
from process_data import amending_data
from transform_data import transform_data

# Ensure logs directory exists
log_dir = "../logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Setting up logging system for debugging and monitoring
logging.basicConfig(
    level=logging.INFO,  # Logging level set to INFO, ignoring DEBUG
    format="%(asctime)s - %(levelname)s - %(message)s",  # Defines format of log messages
    handlers=[
        logging.FileHandler(f"{log_dir}/app.log"),
        logging.StreamHandler()
    ]  # Logs saved for reference when debugging
)

def main():  # Logic for the ETL pipeline
    try:  # Try-except block to handle potential errors
        logging.info("Starting ETL pipeline...")

        # Centralised file paths where data will be saved
        raw_data_path = "../data/flight_data.json"
        filtered_data_path = "../data/filtered_flight_data.json"
        transformed_data_path = "../data/transformed_flight_data.csv"

        # Step 1: Extracting raw data from Copenhagen Optimization
        logging.info("Step 1: Fetching data from the API...")
        fetch_forecast_data()  # Saves data to raw_data_path
        logging.info(f"Data fetched and saved to {raw_data_path}")

        # Step 2: Transforming raw data
        logging.info("Step 2: Filtering and cleaning raw data...")
        amending_data(raw_data_path, filtered_data_path)
        logging.info(f"Filtered data saved to {filtered_data_path}")

        # Step 3: Transform and export to CSV
        logging.info("Step 3: Transforming data and exporting to CSV...")
        transform_data(filtered_data_path, transformed_data_path)
        logging.info(f"Transformed data saved to {transformed_data_path}")

        logging.info("ETL pipeline successfully completed.")

    except Exception as e:  # Catches errors in the try block and logs them
        logging.error(f"An error occurred: {e}", exc_info=True)  # Traceback to the log where error occurred

if __name__ == "__main__":
    main()  # main() is only executed when the script is run directly