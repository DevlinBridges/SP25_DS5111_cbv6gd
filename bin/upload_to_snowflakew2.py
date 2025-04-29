import os
import re
import pandas as pd
from dotenv import load_dotenv
import snowflake.connector

# Load environment variables
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

# Folder with CSVs
upload_folder = "data/"

for file_name in os.listdir(upload_folder):
    # ✅ Only process normalized files
    if file_name.endswith(".csv") and "norm" in file_name.lower():
        print(f"📄 Processing {file_name}...")
        try:
            df = pd.read_csv(os.path.join(upload_folder, file_name))

            # Normalize column names if present
            if 'symbol' in df.columns:
                df = df.rename(columns={
                    "symbol": "TICKER",
                    "price": "PRICE",
                    "price_change": "PRICE_CHANGE",
                    "price_percent_change": "PRICE_PERCENT_CHANGE"
                })

            if 'TICKER' not in df.columns:
                print(f"⚠️ Skipping {file_name} (no TICKER column)")
                continue

            # Parse timestamp from filename
            match = re.search(r'(\d{8}_\d{6})', file_name)
            if match:
                timestamp = pd.to_datetime(match.group(1), format='%Y%m%d_%H%M%S')
            else:
                timestamp = pd.NaT
                print(f"⚠️ Could not extract timestamp from {file_name}")

            # Infer source from file name (e.g., yahoo, wsj)
            source_match = re.search(r'(yahoo|wsj)', file_name, re.IGNORECASE)
            source = source_match.group(1).lower() if source_match else 'unknown'

            # Add metadata
            df['TIMESTAMP'] = timestamp
            df['SOURCE'] = source

            # Prepare insert
            insert_sql = """
                INSERT INTO STOCKS (TICKER, PRICE, PRICE_CHANGE, PRICE_PERCENT_CHANGE, TIMESTAMP, SOURCE)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            data_to_insert = list(df[['TICKER', 'PRICE', 'PRICE_CHANGE', 'PRICE_PERCENT_CHANGE', 'TIMESTAMP', 'SOURCE']].itertuples(index=False, name=None))

            if data_to_insert:
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
