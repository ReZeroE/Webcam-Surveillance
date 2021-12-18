import os
import sys
import subprocess
from constants import PYTHONVERSION
from facial_tracking import Detection

class Runner:
    def __init__(self):
        self.access_granted = False

    def run_program(self):
        try:
            os.mkdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'recordings'))
        except OSError as ex:
            pass

        subprocess.Popen(f"py -{PYTHONVERSION} ./password_prompt.py", shell = True)
        subprocess.Popen(["start", "cmd", "/k", f"py -{PYTHONVERSION} ./integrity_identifier.py"], shell = True)

        detection_obj = Detection()
        detection_obj.run_program()

    def requirements_validation(self):
        subprocess.Popen([f"py -{PYTHONVERSION} ./req_validator.py"], shell = True)


if __name__ == "__main__":
    r = Runner()
    r.requirements_validation() # validates all the required lib and python version
    r.run_program() # runs program