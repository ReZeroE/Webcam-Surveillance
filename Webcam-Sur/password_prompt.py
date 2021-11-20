import os
import sys
import json
import time
from datetime import datetime
from tkinter import *
from tkinter import ttk

from security_measure import security_measure
from integrity_identifier import IntegrityIdentifier

class password_prompt:

    def __init__(self):
        self.win = Tk()
        self.password = StringVar()

        self.access_status_file = "database/access_status.json"
        self.password_file = "database/password.json"
        self.pids_file = "database/pids.json"

        self.access_attempts = 0
        self.access_granted = False

        self.SECURETIME = 21600

    def confirm_passcode(self):
        access_granted = False
        entered_passcode = str(self.password.get())
        print(entered_passcode)
        time_now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        replacement_set = dict()
        
        
        # confirms password
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.password_file), 'r', encoding="utf-8") as rf:
            password_dict = json.load(rf)
            default_passcord = password_dict['passcode']
            self.access_attempts += 1

            if(default_passcord == entered_passcode):
                access_granted = True


        # load to record
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.access_status_file), 'r', encoding="utf-8") as rf:
            gen_dict = json.load(rf)
            access_status_dict = gen_dict['access_status']
            record_dict = gen_dict['access_record']
            
            records = record_dict['records']

            if access_granted:
                access_status_dict['accessed'] = 1
                access_status_dict['last_access_attempt'] = time_now

                records.insert(0, f"Access Granted - {time_now}")
                record_dict['records'] = records
            else:
                access_status_dict['accessed'] = 0
                access_status_dict['last_access_attempt'] = time_now

                records.insert(0, f"Access Denied - {time_now} -> {entered_passcode}")
                record_dict['records'] = records

                if self.access_attempts <= 2:
                    ttk.Label(self.win, text=f"The password you have entered is incorrect. Attempts left: {3 - self.access_attempts}").pack()
                else:
                    ttk.Label(self.win, text=f"The password you have entered is incorrect. Security measure activated.").pack()

            replacement_set['access_status'] = access_status_dict
            replacement_set["access_record"] = record_dict

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.access_status_file), 'w', encoding="utf-8") as wf:
            json.dump(replacement_set, wf, ensure_ascii=False, indent = 4)

        self.access_granted = access_granted

    def prompt_password(self) -> bool:
        self.win.attributes('-fullscreen', True)
        self.win.attributes('-topmost', True)

        entry = Entry(self.win, width=25, textvariable=self.password, show="*")
        entry.pack(pady=((int(self.win.winfo_screenheight()/2) - 100), 0))

        button = ttk.Button(self.win, text="Confirm Password", command=self.confirm_passcode)
        button.pack(pady=10)

        while True:
            # ensure program is on top
            self.win.attributes('-fullscreen', True)
            self.win.attributes('-topmost', True)

            if self.access_granted == True:
                # disable security -> granted access
                return True

            elif self.access_granted == False and self.access_attempts >= 3:
                # activate security measures
                s = security_measure()
                s.activate_security_measure()
                self.access_attempts = 0
                self.win.destroy()

                return False

            self.win.update()
            # self.win.mainloop()

if __name__ == "__main__":
    ii = IntegrityIdentifier()
    ii.load_pid_to_file(os.path.basename(__file__), os.getpid())

    access_granted = False

    while access_granted == False:
        program_runner = password_prompt()
        access_granted = program_runner.prompt_password()