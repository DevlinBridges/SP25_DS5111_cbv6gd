#!/bin/bash

# Update and prep
sudo apt update
sudo apt install -y fonts-liberation libu2f-udev

# Remove old Chrome if needed
sudo apt remove -y google-chrome-stable
sudo rm -f /usr/bin/google-chrome

# Install Chrome v133 (to match ChromeDriver)
wget https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_133.0.5672.126-1_amd64.deb
sudo apt install -y ./google-chrome-stable_133.0.5672.126-1_amd64.deb

# Check install
google-chrome --version
google-chrome --headless --disable-gpu --dump-dom https://example.com/
