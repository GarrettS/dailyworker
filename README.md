Good catch. Those are exactly the kinds of operational details that make the difference between “this worked once for me” and “this works reliably every day.”

Here’s a tightened, practical section set for the README, integrating those missing details:

---

## System Setup

### 1. Install Python 3.11

Python 3.12 fails with Selenium + Chrome on macOS.
Install 3.11 with Homebrew:

```bash
brew install python@3.11
```

Check the path:

```bash
which python3.11
```

Use this path in the plist file.

---

### 2. Grant Full Disk Access

macOS may block automated access to Chrome profiles unless Python has **Full Disk Access**.

Go to:
`System Settings → Privacy & Security → Full Disk Access`
Add `/usr/local/bin/python3.11` (or the path from step 1). (⌘ + SHIFT + G)

---

### 3. ChromeDriver Path

Install ChromeDriver via Homebrew:

```bash
brew install chromedriver
```

Typical path:
`/usr/local/bin/chromedriver`

Set this path in the Python file:

```python
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
```

---

### 4. LaunchAgent Configuration

The LaunchAgent runs the script automatically each morning.

* Copy `daily_worker.plist.template` to:

```
~/Library/LaunchAgents/com.[your_computer_username].daily_worker.plist
```

* Edit the file and set:

  * Your Python 3.11 path
  * Full path to `run_daily_worker.py`

* Load it:

```bash
launchctl load ~/Library/LaunchAgents/com.[your_computer_username].daily_worker.plist
launchctl start com.[your_computer_username].daily_worker
```

To verify:

```bash
launchctl list | grep daily_worker
```

To unload:

```bash
launchctl unload ~/Library/LaunchAgents/com.[your_computer_username].daily_worker.plist
```

---

### 5. Scheduled Wake-Up

LaunchAgents won’t run if the machine is asleep.
To ensure the system is awake before the script runs, schedule a wake event with `pmset`. For example, if the script runs at 7:55 AM:

```bash
sudo pmset repeat wakeorpoweron MTWRFSU 07:55:00
```

This wakes the system five minutes before the form automation runs.

---

### 6. After Reboot

* LaunchAgents **persist after reboot**, but the scheduled wake time does not if power was completely removed (e.g., Mac shut down vs. asleep).
* You may need to re-run the `pmset` command if you fully shut down.
* Check status with:

```bash
pmset -g sched
```

---

### 7. Test the Script

Run manually before relying on automation:

```bash
/usr/local/bin/python3.11 ~/Scripts/run_daily_worker.py
```

Chrome should launch, fill out the form, and submit it.
