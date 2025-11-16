# dailyworker/fallbacks.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
)
import sys
import time

def submit_and_verify(driver):
    """
    Click Submit and confirm via:
      - URL containing /formResponse, or
      - 'Your response has been recorded' text.
    Returns (is_submitted: bool, reason: str).
    """
    submit = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable(
            (By.XPATH,
             "//span[normalize-space()='Submit']/ancestor::div[@role='button']")
        )
    )
    submit.click()

    # URL-based confirmation
    try:
        WebDriverWait(driver, 7).until(EC.url_contains("/formResponse"))
        return True, "formResponse URL seen"
    except TimeoutException:
        pass

    # Text-based confirmation
    try:
        WebDriverWait(driver, 7).until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[contains(., 'Your response has been recorded')]")
            )
        )
        return True, "confirmation text seen"
    except TimeoutException:
        return False, "No formResponse URL and no confirmation text"


def fallback_radios_click_no(driver) -> bool:
    """
    For each *required* radio group where nothing is selected yet,
    click the 'No' option if present.

    Returns True if at least one 'No' was clicked; False otherwise.
    """
    blocks = driver.find_elements(
        By.XPATH,
        "//span[@aria-label='Required question']"
        "/ancestor::div[.//div[@role='radio']][1]"
    )

    print(f"[fallback-radios] required radio blocks found: {len(blocks)}",
          file=sys.stderr)
    clicked_any = False

    for block in blocks:
        radios = block.find_elements(By.XPATH, ".//div[@role='radio']")
        if not radios:
            continue

        has_checked = any(
            r.get_attribute("aria-checked") == "true" for r in radios
        )
        if has_checked:
            continue

        # Find the 'No' radio in this group
        no_radio = None
        for r in radios:
            label = (r.get_attribute("aria-label") or "").strip().lower()
            text  = (r.text or "").strip().lower()
            if label.startswith("no") or text.startswith("no"):
                no_radio = r
                break

        if not no_radio:
            continue

        try:
            driver.execute_script("arguments[0].focus();", no_radio)
            time.sleep(0.2)

            try:
                no_radio.click()
            except ElementClickInterceptedException:
                driver.execute_script("arguments[0].click();", no_radio)

            clicked_any = True
            print("[fallback-radios] clicked 'No' in a required group",
                  file=sys.stderr)

        except (StaleElementReferenceException, ElementClickInterceptedException) as e:
            print(f"[fallback-radios] failed to click 'No' radio: {e}",
                  file=sys.stderr)

    print(f"[fallback-radios] clicked_any={clicked_any}", file=sys.stderr)
    return clicked_any


def fallback_text_inputs_type_ok(driver) -> bool:
    """
    After a failed submit, Google shows inline error blocks with:
      <div role="alert"> ... <span>This is a required question</span> ...
    For each such question, if there is an empty text input/textarea,
    fill it with DEFAULT_REQUIRED_TEXT_ANSWER.

    Returns True if at least one field was filled; False otherwise.
    """
    DEFAULT_REQUIRED_TEXT_ANSWER = "OK"

    alerts = driver.find_elements(
        By.XPATH,
        "//div[@role='alert']//span[contains(., 'This is a required question')]"
    )

    print(f"[fallback-text] required alerts found: {len(alerts)}",
          file=sys.stderr)
    changed_any = False

    for alert in alerts:
        try:
            block = alert.find_element(
                By.XPATH,
                "./ancestor::div[.//input[@type='text'] or .//textarea][1]"
            )
        except Exception:
            continue

        inputs = block.find_elements(
            By.XPATH,
            ".//input[@type='text'] | .//textarea"
        )

        for inp in inputs:
            try:
                current = (inp.get_attribute("value") or "").strip()
                if current:
                    continue

                driver.execute_script("arguments[0].focus();", inp)
                time.sleep(0.2)
                inp.send_keys(DEFAULT_REQUIRED_TEXT_ANSWER)
                changed_any = True
                print("[fallback-text] filled an empty required text input",
                      file=sys.stderr)
            except StaleElementReferenceException:
                continue

    print(f"[fallback-text] changed_any={changed_any}", file=sys.stderr)
    return changed_any


def fix_required_questions(driver) -> bool:
    """
    Try both fallback strategies:
      - required radios: click 'No' in unanswered groups
      - required text inputs: type a default answer

    Returns True if anything was changed; False otherwise.
    """
    changed_radios = fallback_radios_click_no(driver)
    changed_text   = fallback_text_inputs_type_ok(driver)
    return changed_radios or changed_text
