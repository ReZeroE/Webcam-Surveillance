import requests
import os
import sys
import re
import time
import json
import smtplib
from pathlib import Path
from datetime import datetime

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

class AlertEmail:
    def __init__(self):
        self.receiver_emails = ["kevinliu@vt.edu"]

        self.email_title = "Unauthorized Access Detected"
        self.email_content = "Warning -> "

    
    def send_email(self):
        EMAIL_ADDRESS = "sightekbots@gmail.com"
        EMAIL_PASS = "sightekBOTS"

        img_file_name = "test.jpg"
        print(os.path.join(os.path.dirname(os.path.abspath(__file__)), img_file_name))
        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), img_file_name), 'rb') as f:
            img_data = f.read()


        with smtplib.SMTP("smtp.gmail.com", 587) as smtp_conn:
            img_filename = 'test.jpg'
            time_now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

            msg = MIMEMultipart()
            msg['Subject'] = f"{self.email_title} - {time_now}"
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = self.receiver_emails[0]

            with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "database/access_status.json"), 'r', encoding="utf-8") as rf:
                gen_dict = json.load(rf)

            text = MIMEText(json.dumps(gen_dict, sort_keys=False, indent=4))
            msg.attach(text)
            image = MIMEImage(img_data, name=os.path.basename(img_filename))
            msg.attach(image)


            smtp_conn.ehlo()
            smtp_conn.starttls() # encrypt traffic
            smtp_conn.ehlo() # reidentify ourselves with the encrypted traffic

            smtp_conn.login(EMAIL_ADDRESS, EMAIL_PASS)

            # subject = self.email_title
            # body = self.email_content

            # time_now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
            # body += f"unauthorized activity detected on {time_now}"

            # msg = f'Subject: {subject}\n\n{body}'

            # text = MIMEText("test")
            # msg.attach(text)
            # image = MIMEImage(img_data, name=os.path.basename(img_file_name))
            # msg.attach(image)

            for receiving_email in self.receiver_emails:
                smtp_conn.sendmail(EMAIL_ADDRESS, receiving_email, msg.as_string())


if __name__ == "__main__":
    ae = AlertEmail()
    ae.send_email() 
