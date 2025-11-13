## Mountain View Daily Worker Form Automation

Automates submission of the Mountain View Day Worker Center's daily registration form for day laborers.
The Mountain View Day Worker Center requires workers to sign up daily between 6:30–8:30 AM. Missing one day moves you to the back of the queue — about a 12-day process to get to the front, if registering consistently every day.

This script uses **Selenium + ChromeDriver** to open Chrome, fill the form, and submit it automatically each morning using a macOS **LaunchAgent**.

### What It Does

* Opens the MV Daily Worker Google Form with your pre-filled data, and submits it.
* Runs automatically on schedule each morning, even if you forget
* Keeps Chrome open briefly so you can verify it (if testing manually).

```
┌─────────────────────────────────────────────────────────────┐
│               macOS Power Management (pmset)                │
│  Schedules wake at 07:55 with:                              │
│  sudo pmset repeat wakeorpoweron MTWRFS 07:55:00            │
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
│  Located in: ~/Library/LaunchAgents/                        │
│  Defines Python path and script execution schedule          │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│           Python Script (daily_worker.py)                   │
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

### 1. Install Python 3.11

Python 3.12 fails with Selenium and LaunchAgents.
Install 3.11 via Homebrew:

```bash
brew install python@3.11
```

Then confirm with:

```bash
/usr/local/bin/python3.11 --version
```

---

### 2. Install dependencies

```bash
pip3.11 install selenium
brew install chromedriver
```

Find your `chromedriver` path with:

```bash
which chromedriver
```

Use that in the Python file as:

```python
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
```

---

### 3. Give Chrome and Python Full Disk Access

macOS requires this for scheduled, unattended runs.

**System Settings → Privacy & Security → Full Disk Access**
Add:

* **Terminal** (to test manually)
* **Python 3.11** (`/usr/local/bin/python3.11`) (⌘ + SHIFT + G)
* **Google Chrome**
* **chromedriver**

---

### 4. Place the files

```
~/Scripts/run_daily_worker.py
~/Library/LaunchAgents/com.[your_username].dailyworker.plist
```

Each file begins with a comment indicating its expected location.

---

### 5. Load the LaunchAgent

After editing the plist to point to the correct paths, launch and unload with the following commands:

```
To unload (disable):
launchctl bootout gui/$(id -u) ~/Library/LaunchAgents/com.[your_username].dailyworker.plist

To load (enable):
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.[your_username].dailyworker.plist

To check if it’s running:
launchctl print gui/$(id -u)/com.[your_username].run_daily_worker.py
```
---

### 6. Schedule system wake-up (optional but recommended)

macOS can wake automatically before your script runs:

```bash
sudo pmset repeat wakeorpoweron MTWRFS 07:55:00
```

This wakes the system Mon-Sat at 7:55 AM so the script can run at 8:00 AM (they're closed Sundays).
Adjust as needed. To view or clear:

```bash
pmset -g sched
sudo pmset repeat cancel
```

---

### 7. Behavior on reboot

LaunchAgents reload automatically after login.
If you want it to run **before** login, you’d need a LaunchDaemon instead, but that runs as root and can’t access your Chrome user data.
So: let the machine auto-login (System Settings → Users & Groups → Login Options).

---

### 8. Test manually

Run once in Terminal:

```bash
/usr/local/bin/python3.11 ~/Scripts/run_daily_worker.py
```

Chrome should open, load the form, and submit it.
If it closes instantly, verify that the prefilled URL and Chrome profile path exist.

---
