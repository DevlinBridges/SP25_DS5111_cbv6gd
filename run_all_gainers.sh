#!/bin/bash

# === Set full paths ===
PROJECT_DIR="/home/ubuntu/SP25_DS5111_cbv6gd"
PYTHON_BIN="$PROJECT_DIR/env/bin/python"
VENV_ACTIVATE="$PROJECT_DIR/env/bin/activate"
LOG_DIR="$PROJECT_DIR/logs"
DATA_DIR="$PROJECT_DIR/data"

# === Navigate to project root ===
cd "$PROJECT_DIR" || exit 1

# === Activate virtual environment ===
source "$VENV_ACTIVATE"

# === Ensure folders exist ===
mkdir -p "$LOG_DIR"
mkdir -p "$DATA_DIR"

# === Get current timestamp ===
timestamp=$(date +"%Y%m%d_%H%M")

# === Output file locations ===
YAHOO_RAW="$DATA_DIR/ygainers_raw_${timestamp}.csv"
YAHOO_NORM="$DATA_DIR/ygainers_norm"
WSJ_RAW="$DATA_DIR/wsgainers_raw_${timestamp}.csv"
WSJ_NORM="$DATA_DIR/wsgainers_norm"

# === Log Python version/debug info ===
echo "🧠 Using Python: $PYTHON_BIN" >> "$LOG_DIR/run_all.log"
"$PYTHON_BIN" -m pip list >> "$LOG_DIR/run_all.log"

# === Run Yahoo Gainers Collection ===
echo "📈 Running Yahoo gainer scrape..." >> "$LOG_DIR/run_all.log"
$PYTHON_BIN bin/get_gainer.py yahoo "$YAHOO_RAW" "$YAHOO_NORM" >> "$LOG_DIR/run_all.log" 2>&1

# === Run WSJ Gainers Collection ===
echo "📰 Running WSJ gainer scrape..." >> "$LOG_DIR/run_all.log"
$PYTHON_BIN bin/get_gainer.py wsj "$WSJ_RAW" "$WSJ_NORM" >> "$LOG_DIR/run_all.log" 2>&1

# === Log Success Message ===
echo "✅ Gainer data collected at ${timestamp}" >> "$LOG_DIR/run_all.log"

# === Deactivate virtual environment ===
deactivate
