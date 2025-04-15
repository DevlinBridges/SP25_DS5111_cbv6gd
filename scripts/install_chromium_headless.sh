#!/bin/bash

# Update system and install Chromium + matching ChromeDriver
sudo apt update
sudo apt install -y chromium-browser chromium-chromedriver fonts-liberation

# Symlink to make everything Selenium-compatible
sudo ln -sf /usr/bin/chromium-browser /usr/bin/google-chrome
sudo ln -sf /usr/lib/chromium-browser/chromedriver /usr/bin/chromedriver

# Check version and test
google-chrome --version
google-chrome --headless --disable-gpu --dump-dom https://example.com/
