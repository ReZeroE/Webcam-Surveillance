import os
import sys
import json
from datetime import datetime
from tkinter import *
from tkinter import ttk


class password_prompt:

    def __init__(self):
        self.win = Tk()
        self.password = StringVar()

        self.access_status_file = "database/access_status.json"
        self.password_file = "database/password.json"

    def confirm_passcode(self):
        access_granted = False
        entered_passcode = str(self.password.get())
        time_now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        replacement_set = dict()
        
        
        # confirms password
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.password_file), 'r', encoding="utf-8") as rf:
            password_dict = json.load(rf)
            default_passcord = password_dict['passcode']

            if(default_passcord == entered_passcode):
                access_granted = True


        # load to record
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.access_status_file), 'r', encoding="utf-8") as rf:
            gen_dict = json.load(rf)
            access_status_dict = gen_dict['access_status']
            record_dict = gen_dict['access_record']
            
            records = record_dict['records']

            if access_granted:
                access_status_dict['accessed'] = 0
                access_status_dict['last_access_attempt'] = time_now

                records.insert(0, f"Access Granted - {time_now}")
                record_dict['records'] = records
            else:
                access_status_dict['accessed'] = 1
                access_status_dict['last_access_attempt'] = time_now

                records.insert(0, f"Access Denied - {time_now} -> {entered_passcode}")
                record_dict['records'] = records

                ttk.Label(self.win, text="The password you have entered is incorrect. Security measure activated.").pack()

            replacement_set['access_status'] = access_status_dict
            replacement_set["access_record"] = record_dict

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), self.access_status_file), 'w', encoding="utf-8") as wf:
            json.dump(replacement_set, wf, ensure_ascii=False, indent = 4)


        if access_granted:
            sys.exit(0)


    def run_program(self):
        # ensure program is on top
        self.win.attributes('-fullscreen',True)
        self.win.attributes('-topmost', True)
        self.win.update()

        entry = Entry(self.win, width=25, textvariable=self.password, show="*")
        entry.pack(pady=10)

        ttk.Button(self.win, text="Confirm Password", command=self.confirm_passcode).pack()

        self.win.mainloop()

if __name__ == "__main__":
    program_runner = password_prompt()
    program_runner.run_program()