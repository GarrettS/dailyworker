## Mountain View Daily Worker Form Automation

Automates submission of the Mountain View Day Worker Center's daily registration form for day laborers.
The Mountain View Day Worker Center requires workers to sign up between fixed hours (e.g., 6:30–8:30 AM). Missing one day moves you to the back of the queue — often a 10-day wait.
This script uses **Selenium + ChromeDriver** to open Chrome, fill the form, and submit it automatically each morning using a macOS **LaunchAgent**.

### What It Does

* Opens a Google Form (or similar) with your pre-filled data
* Waits for the form to load, then submits
* Runs automatically on schedule each morning, even if you forget
* Keeps Chrome open briefly so you can verify it (if testing manually)

---

## Setup

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

* **Terminal** (if you’ll test manually)
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
launchctl print gui/$(id -u)/com.[your_username].dailyworker
```
---

### 6. Schedule system wake-up (optional but recommended)

macOS can wake automatically before your script runs:

```bash
sudo pmset repeat wakeorpoweron MTWRFSU 07:55:00
```

This wakes the system daily at 7:55 AM so the script can run at, say, 8:00 AM.
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

Would you like me to generate the matching `run_daily_worker.py` and `.plist` templates (with inline location and setup comments) to go with this?
