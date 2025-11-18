# DailyWorker Automation

Automates the early-morning submission of a prefilled Google Form used by the [Mountain View Day Worker Center](https://www.dayworkercentermv.org/)(DWC), where workers like you can register to maintain a position in a queue with the hopes of doing labor for $25/hr.

## Problem
What does the DailyWorker Automation solve?

This script tries to submit the Day Worker Center (DWC) form at **7:00 AM**, detects any failure, notifies you instantly, and keeps Chrome open so you can fix issues before the 8:30 AM cutoff.

## Context
The Day Worker Center daily registration form uses a queue. You, the user, declare your availability each day by filling out the [daily worker form](https://docs.google.com/forms/d/e/1FAIpQLSdYGfA0gaqJBTvqOeprVJLp-NU2B6GGqjamXAbfmQI0_oJWFg/viewform?pli=1&pli=1). 

The center receives the form submission and sets or advances your position in the queue. Each day, you be given a chance to fill out this form and, upon completeion, will be advanced towards the front of the queue. Reaching the front of the queue typically takes about three weeks of consistent daily registrations. You will lose your place in the queue by one of the folllowing two ways:
1. Failing to register before being chosen to work
2. Reaching the head of the queue, and staying there until you are chosen to work.

If you are chosen to work by the DWC, you are dispatched to a job and taken out of the queue. If you fail to register for any day (if you missed it, forgot, etc), you will be taken out of the queue. 

For this reason, it is very important you *do not miss any registration days*, as that will take you out of the queue, and you will have to start all over again. 

It is also important to make it to the job site on time, as failure to do so may result in loss of that job.

The DWC advertises that they give jobs to skilled workers, but in my experience, they do not care (if you have landscaping, moving, painting, or drywall experience, for example, they might not care).

Your best bet to earn money is to register every day.

```
┌─────────────────────────────────────────────────────────────┐
│               macOS Power Management (pmset)                │
│  Schedules wake at 07:55 with:                              │
│  sudo pmset repeat wakeorpoweron MTWRFS 06:59:00            │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     launchd Scheduler                       │
│  System-level process that loads user LaunchAgents at wake  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│           LaunchAgent (daily_worker.plist)                  │          
│ Schedules run_daily_worker.py @ 7:00 AM (post-launchd wake) │
│  Located in: ~/Library/LaunchAgents/                        │
│  Defines Python path and script execution schedule          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│           Python Script (run_daily_worker.py)               │
│  Location: ~/Scripts/                                       │
│  Uses: /usr/local/bin/python3.11                            │
│  Builds form URL, launches Chrome, submits form via Selenium│
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Chrome (Selenium)                         │
│  Loads user profile: /Users/[YOUR_USERNAME]/ChromeProfile   │
│  Submits Mountain View Day Worker Form                      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│           Day Worker Center System                          │
│  Receives form submission                                   │
│  Adds worker to queue                                       │
│  Sends SMS with either: queue number or job detail          │
└─────────────────────────────────────────────────────────────┘
```
--- 

## Features

- Automatic daily submission using macOS `launchd`
- Uses your real Chrome profile (Google login preserved)
- Detects surprise *required* fields and fixes them:
  - Required **radio groups** → tries to find &amp; select field labeled `No`
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

**WARNING:** The Center changes their form frequently and without notice with *required* fields that may appear and disappear. This script handles the unexpected but required fields with a dual-pronged approach:
1. Re-submission with fallbacks
2. Early 7:00 AM submission with SMS/email notice to you, so you have time to manually correct the error (and not be placed at the end of the queue).

If submission fails:

1. Script identifies surprise required fields
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
