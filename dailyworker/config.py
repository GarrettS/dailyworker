# dailyworker/config.py
from urllib.parse import urlencode
import datetime
import os

BASE_URL = (
    "https://docs.google.com/forms/d/e/"
    "1FAIpQLSdYGfA0gaqJBTvqOeprVJLp-NU2B6GGqjamXAbfmQI0_oJWFg/viewform"
)

CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
PROFILE_DIR       = "/Users/<YOUR_USERNAME>/ChromeProfile"
LOGDIR            = "/Users/<YOUR_USERNAME>/Library/Logs"

SEND_IMESSAGE_TO = ""  # e.g. "15551234567"
SEND_EMAIL_TO = ""     # e.g. "you@example.com"

MAX_LOG_BYTES     = 100_000
MAX_LOG_LINES     = 200

# When False: always close Chrome.
# When True: keep Chrome open on failure for manual debugging.
DEBUG_KEEP_OPEN_ON_FAIL = True

# User data
FIRST = "YOUR_FIRST_NAME"
LAST  = "YOUR_LAST_NAME"
PHONE = "YOUR_PHONE_NUMBER"

# Day-of-week constants
MON, TUE, WED, THU, FRI, SAT, SUN = range(7)
TODAY = datetime.date.today().weekday()

# Sentinel: -1 means “no special day logic yet”
DAY_OFF_TODAY    = -1  # you can set to FRI later if you want
DAY_OFF_TOMORROW = -1  # set to THU to make Friday “no” tomorrow, etc.

AVAILABLE_TODAY    = "No" if TODAY == DAY_OFF_TODAY    else "Yes"
AVAILABLE_TOMORROW = "No" if TODAY == DAY_OFF_TOMORROW else "Yes"

# Build form params
PARAMS = {
    "entry.1168736198": FIRST,
    "entry.1251849264": LAST,
    "entry.1602403548": PHONE,
    "entry.1064271633": "",          # Anything else we should know?
    "entry.284217838": "English",
    "entry.466782773": AVAILABLE_TODAY,     # Available today?
    "entry.1282757110": AVAILABLE_TOMORROW, # Available tomorrow?
    "entry.962240141": "No",         # Do you have COVID symptoms?
    "entry.91204779":  "Yes",        # Have you been in contact with someone with COVID?
    "entry.7004839":   "Yes/Si",     # Do you have a car?
}

WORK_TYPES = [
    "Domestic Labor/Trabajo Domestico",
    "Heavy Physical labor/Trabajo Fisico",
]
for w in WORK_TYPES:
    PARAMS.setdefault("entry.1397227875", []).append(w)

PREFILLED_URL = f"{BASE_URL}?{urlencode(PARAMS, doseq=True)}"

STATUS_LOG_PATH = os.path.join(LOGDIR, "daily_worker_status.log")
