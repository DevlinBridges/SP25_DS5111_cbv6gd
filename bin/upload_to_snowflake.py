import os
import re
import pandas as pd
from dotenv import load_dotenv
import snowflake.connector

# Load environment variables from .env file
load_dotenv()

# Connect to Snowflake
conn = snowflake.connector.connect(
    account=os.getenv("SNOWFLAKE_ACCOUNT"),
    user=os.getenv("SNOWFLAKE_USER"),
    password=os.getenv("SNOWFLAKE_PASSWORD"),
    role=os.getenv("SNOWFLAKE_ROLE"),
    warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
    database=os.getenv("SNOWFLAKE_DATABASE"),
    schema=os.getenv("SNOWFLAKE_SCHEMA"),
)
cs = conn.cursor()

# Upload directory
upload_folder = "data/"

# Loop through each CSV file in the upload folder
for file_name in os.listdir(upload_folder):
    if file_name.endswith(".csv"):
        print(f"📄 Processing {file_name}...")
        try:
            df = pd.read_csv(os.path.join(upload_folder, file_name))

            # Fix columns (only for normalized files)
            if 'symbol' in df.columns:
                df = df.rename(columns={
                    "symbol": "TICKER",
                    "price": "PRICE",
                    "price_change": "PRICE_CHANGE",
                    "price_percent_change": "PRICE_PERCENT_CHANGE"
                })

            # If TICKER column missing after renaming, skip
            if 'TICKER' not in df.columns:
                print(f"⚠️ Skipping {file_name} (no TICKER column)")
                continue

            # Add a TIMESTAMP column from the filename if possible
            match = re.search(r'(\d{8}_\d{6})', file_name)
            if match:
                timestamp = pd.to_datetime(match.group(1), format='%Y%m%d_%H%M%S')
                df['TIMESTAMP'] = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            else:
                print(f"⚠️ Could not extract timestamp from {file_name}")
                df['TIMESTAMP'] = None

            # If any row has NaT/NaN, convert to None
            df['TIMESTAMP'] = df['TIMESTAMP'].where(pd.notnull(df['TIMESTAMP']), None)

            # Prepare data for insert as all strings (TIMESTAMP must be str, not datetime)
            data_to_insert = [
                (
                    row['TICKER'],
                    row['PRICE'],
                    row['PRICE_CHANGE'],
                    row['PRICE_PERCENT_CHANGE'],
                    row['TIMESTAMP']
                )
                for _, row in df.iterrows()
            ]

            if data_to_insert:
                insert_sql = """
                    INSERT INTO STOCKS (TICKER, PRICE, PRICE_CHANGE, PRICE_PERCENT_CHANGE, TIMESTAMP)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cs.executemany(insert_sql, data_to_insert)
                print(f"✅ Successfully inserted {len(data_to_insert)} rows from {file_name}")
            else:
                print(f"⚠️ No data to insert from {file_name}")

        except Exception as e:
            print(f"❌ Failed processing {file_name}: {e}")

# Cleanup
cs.close()
conn.close()

print("🎉 Upload complete.")
