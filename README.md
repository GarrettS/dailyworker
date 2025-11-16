# DailyWorker Automation

Automates the early-morning submission of a prefilled Google Form used by the Day Worker Center.

The Center changes their form frequently and without notice — fields appear, disappear, or suddenly become *required*.  
This script submits at **7:00 AM**, detects any failure, notifies you instantly, and keeps Chrome open so you can fix issues before the 8:30 AM cutoff.

--- 

## Features

- Automatic daily submission using macOS `launchd`
- Uses your real Chrome profile (Google login preserved)
- Detects surprise *required* fields and fixes them:
  - Required **radio groups** → selects “No”
  - Required **text inputs** → types `"OK"`
- Captures screenshot + HTML after each run
- Logs every submission (with automatic truncation)
- Optional notifications:
  - macOS Notification Center
  - iMessage
  - Email (Apple Mail)
- Keeps Chrome open on failure for inspection

---

## Requirements

- macOS  
- Python 3.11+  
- Chrome + matching ChromeDriver  
- AppleScript enabled (for notifications)

---

## Installation

Clone the repo:

```bash
git clone https://github.com/GarrettS/dailyworker.git
cd dailyworker
```

Create a venv:

```bash
python3.11 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Project Structure

```
dailyworker/
    dailyworker/
        __init__.py
        config.py
        main.py
        submitform.py
        notify.py
        logging.py
    launchagent/
        com.dailyworker.autosubmit.plist
    run_daily_worker.py
    README.md
```

### Module overview

- **config.py** — All user-editable settings  
- **main.py** — Main workflow runner  
- **submitform.py** — Submit logic and fallback handlers  
- **notify.py** — macOS notification, iMessage, Apple Mail  
- **logging.py** — Logging utilities + truncation  
- **run_daily_worker.py** — Entry point used by `launchd`  
- **launchagent plist** — Schedules the run at 7:00 AM  

---

## Configuration

Edit:

```
dailyworker/dailyworker/config.py
```

Example:

```python
FORM_URL = "https://docs.google.com/forms/..."

PROFILE_DIR = "/Users/YOUR_USER/ChromeProfile"
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
LOGDIR = "/Users/YOUR_USER/Library/Logs/DailyWorker"

SEND_IMESSAGE_TO = None
SEND_EMAIL_TO    = None

DEFAULT_REQUIRED_TEXT_ANSWER = "OK"
DEBUG_KEEP_OPEN_ON_FAIL = True
```

Keep personal phone numbers and emails **out of the repo**.

---

## Manual Run

```bash
./run_daily_worker.py
```

Or:

```bash
python3 dailyworker/main.py
```

---

## Setting up launchd

Copy the LaunchAgent:

```bash
cp launchagent/com.dailyworker.autosubmit.plist ~/Library/LaunchAgents/
```

Load it:

```bash
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.dailyworker.autosubmit.plist
```

Check status:

```bash
launchctl print gui/$(id -u)/com.dailyworker.autosubmit
```

Unload:

```bash
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.dailyworker.autosubmit.plist
```

---

## macOS Wake Scheduling

macOS supports **one** repeating wake schedule.

Set:

```bash
sudo pmset repeat wakeorpoweron MTWRFS 06:59:00
```

Check:

```bash
pmset -g sched
```

Clear:

```bash
sudo pmset repeat cancel
```

Every new `pmset repeat` replaces the previous one.

---

## Logs & Evidence

Everything is stored in:

```
~/Library/Logs/DailyWorker/
```

You’ll see:

- `daily_worker_status.log`
- `daily_worker_YYYYMMDD-HHMMSS.html`
- `daily_worker_YYYYMMDD-HHMMSS.png`

Tail the log in real time:

```bash
tail -f ~/Library/Logs/DailyWorker/daily_worker_status.log
```

Logs auto-truncate when they exceed your configured size.

---

## Fallback Behavior

If submission fails:

1. Script identifies required fields Google added
2. Auto-answers:
   - Required radios → “No”
   - Required text inputs → `"OK"`
3. Attempts a second submission
4. If it still fails:
   - Chrome remains open
   - Screenshot and HTML are saved
   - Notifications are sent

Running early gives you time to fix anything manually.

---

## Notes on Google Form Instability

The Day Worker Center regularly:

- Adds new required fields without notice  
- Removes required flags shortly after  
- Inserts malformed blocks  
- Rearranges fieldsets

This script is designed to absorb most of that chaos.

Anything it can’t fix automatically is surfaced immediately to you with Chrome left open.

---

## License

MIT License.
