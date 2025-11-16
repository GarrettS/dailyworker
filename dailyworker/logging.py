# dailyworker/logging_utils.py
import os
import datetime

from .config import STATUS_LOG_PATH, MAX_LOG_BYTES, MAX_LOG_LINES


def truncate_status_log_if_needed() -> None:
    if not os.path.exists(STATUS_LOG_PATH):
        return
    if os.path.getsize(STATUS_LOG_PATH) <= MAX_LOG_BYTES:
        return

    with open(STATUS_LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    tail = lines[-MAX_LOG_LINES:]
    now_ts = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    with open(STATUS_LOG_PATH, "w", encoding="utf-8") as f:
        f.write(f"{now_ts} | LOG TRUNCATED — kept last {len(tail)} lines\n\n")
        f.writelines(tail)


def append_status_line(ts: str, is_submitted: bool, url: str, reason: str) -> None:
    line = f"{ts} | {'OK' if is_submitted else 'FAIL'} | {url} | {reason}\n"
    with open(STATUS_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(line)
