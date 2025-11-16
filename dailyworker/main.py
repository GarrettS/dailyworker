# dailyworker/main.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import os
import sys

from .config import (
    CHROMEDRIVER_PATH,
    PROFILE_DIR,
    LOGDIR,
    PREFILLED_URL,
    SEND_IMESSAGE_TO,
    SEND_EMAIL_TO,
    DEBUG_KEEP_OPEN_ON_FAIL,
)
from .notify import notify_nc, notify_imessage, notify_mail
from .submitform import submit_and_verify, fix_required_questions
from .logging import truncate_status_log_if_needed, append_status_line


def main() -> None:
    now = datetime.datetime.now()
    ts = now.strftime("%Y%m%d-%H%M%S")

    png_path  = os.path.join(LOGDIR, f"daily_worker_{ts}.png")
    html_path = os.path.join(LOGDIR, f"daily_worker_{ts}.html")

    print(f"Running {__file__} at {now}", file=sys.stderr)
    print(PREFILLED_URL, file=sys.stderr)

    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={PROFILE_DIR}")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=Service(CHROMEDRIVER_PATH),
                              options=chrome_options)

    is_submitted = False
    reason = "Not attempted"

    try:
        driver.get(PREFILLED_URL)

        # Ensure the first field is present
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "entry.1168736198"))
        )

        # First attempt
        is_submitted, reason = submit_and_verify(driver)

        # Fallback if needed
        if not is_submitted:
            try:
                changed = fix_required_questions(driver)
                if changed:
                    is_submitted, reason = submit_and_verify(driver)
                    if is_submitted:
                        reason = "Required questions auto-answered and resubmitted OK"
                else:
                    reason = (
                        "No unanswered required radios/text inputs; submit still failed"
                    )
            except Exception as e:
                is_submitted = False
                reason = f"Fallback error: {e!r}"

    except Exception as e:
        is_submitted = False
        reason = f"Fatal exception before/around submit: {e!r}"

    finally:
        # Evidence
        try:
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(driver.page_source)
        except Exception:
            pass

        try:
            driver.save_screenshot(png_path)
        except Exception:
            pass

        # Log
        truncate_status_log_if_needed()
        current_url = getattr(driver, "current_url", "")
        append_status_line(ts, is_submitted, current_url, reason)

        # Notifications
        title = f"Daily Worker @{now.strftime('%H:%M')}"
        msg   = "Submitted OK." if is_submitted else "FAILED — check screenshot/logs."

        notify_nc(title, msg)
        if SEND_IMESSAGE_TO:
            notify_imessage(SEND_IMESSAGE_TO, f"{title}: {msg}")
        if SEND_EMAIL_TO:
            body = (
                f"{msg}\n\n"
                f"URL:  {PREFILLED_URL}\n"
                f"PNG:  {png_path}\n"
                f"HTML: {html_path}\n"
            )
            notify_mail(SEND_EMAIL_TO, title, body)

        # Close only on success or when debugging is off
        if is_submitted or not DEBUG_KEEP_OPEN_ON_FAIL:
            try:
                driver.quit()
            except Exception:
                pass
        else:
            print("[main] DEBUG_KEEP_OPEN_ON_FAIL is True; leaving Chrome open.",
                  file=sys.stderr)
