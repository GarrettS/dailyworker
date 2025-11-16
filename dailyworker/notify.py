# dailyworker/notify.py
import subprocess

def notify_nc(title: str, message: str) -> None:
    safe_title = title.replace('"', "'")
    safe_msg   = message.replace('"', "'")
    script = f'display notification "{safe_msg}" with title "{safe_title}"'
    subprocess.run(["osascript", "-e", script], check=False)


def notify_imessage(recipient: str | None, text: str) -> None:
    if not recipient:
        return
    safe_text = text.replace('"', "'")
    osa = f'''
    tell application "Messages"
        set targetService to 1st service whose service type = iMessage
        set targetBuddy to buddy "{recipient}" of targetService
        send "{safe_text}" to targetBuddy
    end tell
    '''
    subprocess.run(["osascript", "-e", osa], check=False)


def notify_mail(to_addr: str | None, subject: str, body: str) -> None:
    if not to_addr:
        return
    safe_body = body.replace('"', "'")
    osa = f'''
    tell application "Mail"
        set newMessage to make new outgoing message with properties {{subject:"{subject}", content:"{safe_body}" & return & return}}
        tell newMessage
            make new to recipient at end of to recipients with properties {{address:"{to_addr}"}}
        end tell
        send newMessage
    end tell
    '''
    subprocess.run(["osascript", "-e", osa], check=False)
