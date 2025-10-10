from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sys, datetime
import time

print(f"Running {__file__} at {datetime.datetime.now()}", file=sys.stderr)

CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
PREFILLED_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdYGfA0gaqJBTvqOeprVJLp-NU2B6GGqjamXAbfmQI0_oJWFg/viewform?pli=1&pli=1&entry.1168736198=Garrett&entry.1251849264=Smith&entry.1602403548=4157703258&entry.1064271633=&entry.284217838=English&entry.1397227875=Domestic+Labor%2FTrabajo+Domestico&entry.1397227875=Heavy+Physical+labor%2FTrabajo+Fisico&entry.466782773=Yes&entry.1282757110=Yes&entry.962240141=No&entry.91204779=Yes&entry.7004839=Yes%2FSi"

chrome_options = Options()
chrome_options.add_argument("user-data-dir=/Users/garrettsmith/ChromeProfile")
chrome_options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH), options=chrome_options)

# Load page
driver.get(PREFILLED_URL)

# Wait until the first input is present (ensures page loaded)
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "entry.1168736198"))
)
submit_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='Submit']"))
)
submit_button.click()
time.sleep(30)

