from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = "/snap/chromium/current/usr/lib/chromium-browser/chrome"

print("🔍 Launching ChromeDriver...")
driver = webdriver.Chrome(service=Service(), options=options)

try:
    print("🌐 Navigating to Yahoo Finance gainers...")
    driver.set_page_load_timeout(60)
    driver.get("https://finance.yahoo.com/gainers")
    time.sleep(10)
    print("✅ Page loaded. First 500 characters of HTML:")
    print(driver.page_source[:500])
finally:
    driver.quit()
    print("🛑 ChromeDriver session ended.")
