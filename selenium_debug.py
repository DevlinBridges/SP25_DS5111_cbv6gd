from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.binary_location = "/usr/bin/google-chrome"

driver = webdriver.Chrome(service=Service(), options=options)
driver.get("https://www.google.com")
print("✅ Chrome launched successfully")
driver.quit()
