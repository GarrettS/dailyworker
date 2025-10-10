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
