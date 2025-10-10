# dailyworker
Mountain View Daily Worker Center — Form Automation

# Daily Worker Automation

This repository automates filling out the time-sensitive "daily worker" form using Python + Selenium and macOS LaunchAgents.

---

## Overview

- `run_daily_worker.py` – Python script that opens Chrome, navigates to the prefilled form URL, fills it automatically, and submits it.
- `daily_worker.plist.template` – macOS LaunchAgent template to run the script automatically at a scheduled time (e.g., 8:00 AM).
- Uses `chromedriver` to control Chrome via Selenium.
- Designed for macOS, Intel or Apple Silicon.

> ⚠️ Paths in the plist and script must be updated to match your own system.

---

## Setup

### 1. Install dependencies

```bash
# Homebrew Python 3.11 is recommended
brew install python@3.11

# Install Selenium
python3 -m pip install selenium

# Install ChromeDriver (version matching your Chrome)
brew install chromedriver
```

1.1 Install Python 3.11

This script requires Python 3.11. It will fail under Python 3.12 due to Selenium or ChromeDriver compatibility issues.
If you don’t already have Python 3.11, install it with Homebrew:
```
brew install python@3.11
```

Then verify it’s available:
```
python3.11 --version
```

Make sure your plist file explicitly calls /usr/local/bin/python3.11.
### 2. Configuration 
run_daily_worker.py → ~/Scripts/run_daily_worker.py

daily_worker.plist.template → ~/Library/LaunchAgents/com.[your_username].daily_worker.py.plist

Replace `[your_username]` with your macOS username.

### 3. Editing the plist
Open com.[your_username].daily_worker.py.plist and update:

<key>ProgramArguments</key>
<array>
    <string>/usr/local/bin/python3.11</string> <!-- path to your Python -->
    <string>/Users/[your_username]/Scripts/run_daily_worker.py</string>
</array>

<key>Label</key>
<string>com.[your_username].daily_worker.py</string>

(No need to adjust `<StartCalendarInterval>` hour/minute to your preferred time (daily worker center takes requests from 6:30 AM – 8:30 AM).)

### 5. Test Python Script Works
Before relying on the scheduler:

/usr/local/bin/python3.11 ~/Scripts/run_daily_worker.py

Ensure Chrome opens, fills, and submits the form as expected.

### 6. Notes:

`PREFILLED_URL` is defined in the Python script. You can edit it there for testing.

Make sure Chrome can launch with the profile specified in user-data-dir.

The system uses a new Chrome session each time, so caching doesn’t affect execution.

If something goes wrong, check logs (~/Library/Logs/run_daily_worker.err) and make sure paths in plist/script match.
