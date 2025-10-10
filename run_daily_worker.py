from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlencode
import urllib.parse
import sys, datetime
import time

print(f"Running {__file__} at {datetime.datetime.now()}", file=sys.stderr)

CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
# --- User-configurable variables ---
FIRST = "YOUR_FIRST_NAME"
LAST = "YOUR_LAST_NAME"
PHONE = "YOUR_PHONE_NUMBER"
LANGUAGE = "English"

# --- Build query parameters ---
base_url = "https://docs.google.com/forms/d/e/1FAIpQLSdYGfA0gaqJBTvqOeprVJLp-NU2B6GGqjamXAbfmQI0_oJWFg/viewform"

params = {
    "entry.1168736198": FIRST,
    "entry.1251849264": LAST,
    "entry.1602403548": PHONE,
    "entry.1064271633": "",
    "entry.284217838": "English",
    "entry.466782773": "Yes",
    "entry.1282757110": "Yes",
    "entry.962240141": "No",
    "entry.91204779": "Yes",
    "entry.7004839": "Yes",
}
WORK_TYPES = [
    "Domestic Labor/Trabajo Domestico",
    "Heavy Physical labor/Trabajo Fisico"
]

# Add work type checkboxes — repeated field
for work_type in WORK_TYPES:
    params.setdefault("entry.1397227875", [])
    params["entry.1397227875"].append(work_type)

PREFILLED_URL = f"{base_url}?{urlencode(params, doseq=True)}"

chrome_options = Options()

# This form requires the user to be signed into his Google account.
chrome_options.add_argument("user-data-dir=/Users/YOUR_USERNAME/ChromeProfile")
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=chrome_options)

# Load page
driver.get(PREFILLED_URL)

# Wait until the first input is present (ensures page loaded)
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "entry.1168736198"))
)
submit_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//div[@role='button']//span[contains(text(),'Submit')]"))
)
submit_button.click()
time.sleep(30)

