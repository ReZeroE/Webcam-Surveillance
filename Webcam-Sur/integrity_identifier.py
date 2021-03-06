import os
import sys
import json
import psutil
import subprocess
from time import sleep
from constants import PYTHONVERSION

class IntegrityIdentifier:

    def __init__(self):
        self.program_integrity_intact = True
        self.record_dict = dict()
        self.pids_path = "database/pids.json"
        self.access_status_file = "database/access_status.json"


    def load_pid_to_file(self, name, pid):
        temp_record_dict = dict()
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.pids_path), 'r', encoding="utf-8") as rf:
            temp_record_dict = json.load(rf)

        temp_record_dict[name] = pid
        
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.pids_path), 'w', encoding="utf-8") as wf:
            json.dump(temp_record_dict, wf, ensure_ascii=False, indent = 4)
        

    def check_program_integrity(self, suppress_pass_prompt=False, suppress_facial_tracking=False):
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.pids_path), 'r', encoding="utf-8") as rf:
            self.record_dict = json.load(rf)

        restart_needed = []
        for process_name, pid in self.record_dict.items():
            if psutil.pid_exists(pid) == False and process_name != "placeholder":

                if suppress_facial_tracking and process_name == "facial_tracking.py":
                    continue
                elif suppress_pass_prompt and process_name == "password_prompt.py":
                    continue
                else:
                    restart_needed.append(process_name)

        print(f"Restart needed: {restart_needed}")
        return restart_needed

    def restart_script(self, restart_list):
        if self.get_access_status() == 1:
            print("Access granted. Integrity indentifier halted...")
            sys.exit(0)

        for script in restart_list:
            if script == "password_prompt.py":
                subprocess.Popen(f"py -{PYTHONVERSION} ./password_prompt.py", shell = True)
            elif script == "facial_tracking.py":
                subprocess.Popen(f"py -{PYTHONVERSION} ./facial_tracking.py", shell = True)

    def get_access_status(self):
        status_dict = dict()
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.access_status_file), 'r', encoding="utf-8") as rf:
            status_dict = json.load(rf)

        return status_dict['access_status']['accessed']


if __name__ == "__main__":
    # wait for other program's initialization
    sleep(10)

    ii = IntegrityIdentifier()
    while True:
        sleep(3)
        restart_list = ii.check_program_integrity(suppress_pass_prompt=True, suppress_facial_tracking=False)

        if len(restart_list) == 0:
            pass
        else:
            ii.restart_script(restart_list)
            

