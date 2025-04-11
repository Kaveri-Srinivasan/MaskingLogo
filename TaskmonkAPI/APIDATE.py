import os
import logging
import pandas as pd
from datetime import datetime
from taskmonk import TaskMonkClient

# Setup logging
level = logging.DEBUG
format = '  %(message)s'
handlers = [logging.FileHandler('logger.log'), logging.StreamHandler()]
logging.basicConfig(level=level, format=format, handlers=handlers)

# Project Configuration
project_id = "4519"
output_dir = "C:\\Users\\kaveri.s\\taskmonk_batches"
os.makedirs(output_dir, exist_ok=True)

# Initialize TaskMonkClient
client = TaskMonkClient(
    "https://preprod.taskmonk.io",
    project_id=project_id,
    client_id='K1J6Vf9V6UuZcTvjkCtOUeetI6Dz1xiG',
    client_secret='EgZpJ9PPtq2l9quZCgFlppKgZg7gI3uHDV9tJx7fgjxIaetCclXQWOczfuojESRA'
)

# Get all batches inside the project
batches = client.get_project_batches()

if not batches:
    logging.info("No batches found in the project.")
else:
    logging.info(f"Found {len(batches)} batches. Retrieving date formats...")

    for batch in batches:
        batch_id = batch["id"]
        output_path = os.path.join(output_dir, f"batch_{batch_id}.csv")

        try:
            # Download batch CSV
            client.get_batch_and_user_output(batch_id, output_path, output_format='CSV')
            logging.info(f'Batch {batch_id} output saved at {output_path}')

            # Read CSV with multiple encoding fallbacks
            try:
                df = pd.read_csv(output_path, encoding="utf-8")
            except UnicodeDecodeError:
                logging.warning(f"UTF-8 decoding failed for batch {batch_id}. Trying ISO-8859-1...")
                df = pd.read_csv(output_path, encoding="ISO-8859-1")

            # Check if the required column exists
            if "L1_U1_Completion_Date" not in df.columns:
                logging.warning(f"Batch {batch_id} does not contain 'L1_U1_Completion_Date'. Skipping...")
                continue

            # Print first few values in terminal
            logging.info(f"Sample L1_U1_Completion_Date values from batch {batch_id}:")
            print(df["L1_U1_Completion_Date"].head(10))  # Print first 10 values

            # Check for NaN values
            missing_dates = df["L1_U1_Completion_Date"].isna().sum()
            logging.info(f"Batch {batch_id}: {missing_dates} missing date values.")

        except Exception as e:
            logging.error(f'Failed to process batch {batch_id}: {e}')
