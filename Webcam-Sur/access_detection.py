from pynput.mouse import Listener as mouse_listener
from pynput.keyboard import Listener as key_listener
from datetime import datetime
from password_prompt import password_prompt
import time

import pyautogui
import time

from ctypes import *

class AccessMonitor:
    def __init__(self):
        self.program_start_time = time.time()

        self.mouse_movement_time = self.program_start_time
        self.mouse_movement = False

        self.security_passed = False

        self.password_prompt_obj = password_prompt()


    def on_move_mouse(self, x, y):
        if self.mouse_movement == False:
            self.mouse_movement = True
            curr_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            print(f"{curr_time} >>> Unidentified mouse click detected. Security measure pending activation.")
            self.mouse_movement_time = time.time()

            self.security_passed = self.password_prompt_obj.prompt_password()

        if self.security_passed == False:
            self.activate_security_measure()


    def on_click_mouse(self, x, y, button, pressed):
        if self.mouse_movement == False:
            self.mouse_movement = True
            curr_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            print(f"{curr_time} >>> Unidentified mouse click detected. Security measure pending activation.")
            self.mouse_movement_time = time.time()

            self.security_passed = self.password_prompt_obj.prompt_password()

        if self.security_passed == False:
            self.activate_security_measure()


    def on_scroll_mouse(self, x, y, dx, dy):
        if self.mouse_movement == False:
            self.mouse_movement = True
            curr_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            print(f"{curr_time} >>> Unidentified mouse click detected. Security measure pending activation.")
            self.mouse_movement_time = time.time()

            self.security_passed = self.password_prompt_obj.prompt_password()

        if self.security_passed == False:
            self.activate_security_measure()


    def activate_security_measure(self):
        print("Security Measure activated...")

        
    def detection_start(self):
        with mouse_listener(on_move=self.on_move_mouse, on_click=self.on_click_mouse, on_scroll=self.on_scroll_mouse) as mouse_monitor:
            mouse_monitor.join()


def run_detector():
    monitor = AccessMonitor()
    monitor.detection_start()



if __name__ == "__main__":
    run_detector()
