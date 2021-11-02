from pynput import mouse
from pynput.mouse import Listener as mouse_listener
from pynput.keyboard import Listener as key_listener
from datetime import datetime
from threading import Timer
import msvcrt
import random
from constants import PASSCODE
import sys
import os
import time

import pyautogui
import time

pyautogui.FAILSAFE = False

from access_blocker import AccessBlocker
from ctypes import *

import subprocess

security_bypass = False

class AccessMonitor:
    def __init__(self):
        self.program_start_time = time.time()

        self.mouse_movement_time = self.program_start_time
        self.mouse_movement = False

        self.key_click = False
        self.key_click_count = 0

        self.passcode = ''
        self.passcode_correct = False

        self.security_passed = False
        self.key_security_passed = False

    def on_move_mouse(self, x, y):
        severity = self.compute_severity()
        if severity == 1:
            return False

        if self.mouse_movement == False:
            curr_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            print(f"{curr_time} >>> Unidentified mouse movement detected. Security measure pending activation.")
            self.mouse_movement_time = time.time()

        self.mouse_movement = True


    def on_click_mouse(self, x, y, button, pressed):
        severity = self.compute_severity()
        if severity == 1:
            return False

        if self.mouse_movement == False:
            curr_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            print(f"{curr_time} >>> Unidentified mouse click detected. Security measure pending activation.")
            self.mouse_movement_time = time.time()
    
        self.mouse_movement = True


    def on_scroll_mouse(self, x, y, dx, dy):
        severity = self.compute_severity()
        if severity == 1:
            return False

        if self.mouse_movement == False:
            curr_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            print(f"{curr_time} >>> Unidentified mouse scroll detected. Security measure pending activation.")
            self.mouse_movement_time = time.time()

        self.mouse_movement = True


    def on_click_key(self, key):
        if self.key_click == False:
            curr_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            print(f"{curr_time} >>> Key click detected. Examining input for passcode.")
            self.key_click = True

        try:
            self.key_click_count += 1
            self.passcode += key.char
        except AttributeError:
            self.activate_security_measure()

        if self.key_click_count == len(PASSCODE):
            self.check_passcode()


    def on_release_key(self, key):
        pass

    
    def check_passcode(self):
        global security_bypass
        curr_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        if self.passcode == PASSCODE:

            print(f"{curr_time} >>> Passcode confirmed! Security measure deactivating...")
            security_bypass = True
            self.security_passed = True

        else:
            print(f"{curr_time} >>> Passcode incorrect. Security measure activating...")
            self.activate_security_measure()


    def compute_severity(self):
        curr_time = time.time()

        if self.security_passed == True:
            self.key_security_passed = True
            return 1

        if curr_time - self.mouse_movement_time > 6000:
            curr_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            print(f"{curr_time} >>> Security measure has been reset ({curr_time - self.mouse_movement_time} sec)")

            self.mouse_movement = False
            self.key_click = False
            self.key_click_count = 0
            self.program_start_time = self.mouse_movement


        if curr_time - self.mouse_movement_time > 10 and self.mouse_movement_time != self.program_start_time:
                return 1
        else:
            return 0

    def activate_security_measure(self):
        print("Security Measure activated...")

        # subprocess.run("start notepad why-are-you-using-my-computer.txt", shell=True)

        # blocker 
        curr = time.time()
        while time.time() - curr < 10:
            pyautogui.moveTo(0, 0, duration = 0.001)

    def detection_start(self):

        with mouse_listener(on_move=self.on_move_mouse, on_click=self.on_click_mouse, on_scroll=self.on_scroll_mouse) as mouse_monitor:
            with key_listener(on_press=self.on_click_key, on_release=self.on_release_key) as key_monitor:
                mouse_monitor.join()

                if mouse_monitor.running == True:
                    key_monitor.join()
                elif self.security_passed == False and self.key_security_passed == False:
                    self.activate_security_measure()


def run_detector():
    while security_bypass == False:
        monitor = AccessMonitor()
        monitor.detection_start()

        if security_bypass == False:
            print("Access detection paused...")
            time.sleep(5)


if __name__ == "__main__":
    run_detector()
