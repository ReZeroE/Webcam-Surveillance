import os
import sys
import subprocess
from facial_tracking import Detection

class Runner:
    def __init__(self):
        self.access_granted = False

    def run_program(self):
        subprocess.Popen(["start", "cmd", "/k", "py -3.6 ./password_prompt.py"], shell = True)
        subprocess.Popen(["start", "cmd", "/k", "pythonw ./integrity_identifier.pyw"], shell = True)

        detection_obj = Detection()
        detection_obj.run_program()


if __name__ == "__main__":
    r = Runner()
    r.run_program()