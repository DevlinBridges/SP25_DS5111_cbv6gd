#!/bin/bash

# Navigate to project root
cd /home/ubuntu/SP25_DS5111_cbv6gd || exit

# Activate virtual environment
source ~/env/bin/activate

# Ensure logs folder exists
mkdir -p logs

# Get timestamp
timestamp=$(date +"%Y%m%d_%H%M")

# Run Yahoo Gainers
python bin/get_gainer.py yahoo data/ygainers_raw_${timestamp}.csv data/ygainers_norm

# Run WSJ Gainers
python bin/get_gainer.py wsj data/wsgainers_raw_${timestamp}.csv data/wsgainers_norm

# Log success
echo "✅ Gainer data collected at ${timestamp}" >> logs/run_all.log

# Deactivate venv
deactivate
