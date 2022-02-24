######################################
#     Developed By DarkKnight        #
######################################

import pandas as pd
import smtplib


SENDER_EMAIL = 'YOUR_EMAIL'
SENDER_PASS = 'YOUR_PASSWORD'
SUBJECT = 'YOUR SUBJECT LIE HERE'
TEMPLATE_PATH = './email-template.txt'
DATA_PATH = './data.csv'
NAME_HEADER = 'Name'
EMAIL_HEADER = 'Email'
LINK_HEADER = 'Link'

EMAIL_TEXT = f"""\
From: {SENDER_EMAIL}
To: TO
Subject: {SUBJECT}

BODY
"""


class EmailSender:
    def __init__(self, sender_email, sender_pass):
        self.sender_email = sender_email

        try:
            self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            self.server.ehlo()
            self.server.login(sender_email, sender_pass)
        except Exception as e:
            print("***Can't login to this gmail***")
            print(e)

        self.getTemplate(TEMPLATE_PATH)

    def __del__(self):
        self.server.close()
    
    def getTemplate(self, template_path):
        with open(template_path, 'r') as file:
            self.template = ''.join(file.readlines())

    def fillTemplate(self, name, link):
        return self.template.replace('NAME', name).replace('LINK', link)

    def getEmailText(self, to, name, link):
        body = self.fillTemplate(name, link)
        return EMAIL_TEXT.replace('TO', to).replace('BODY', body)

    def send(self, to, name, link):
        try:
            email_text = self.getEmailText(to, name, link)
            self.server.sendmail(self.sender_email, to, email_text)
            print(f'[+] Successfully sent to: {name}')
        except:
            print(f'[-] Failed sent to: {name}')



emailSender = EmailSender(SENDER_EMAIL, SENDER_PASS)

data = pd.read_csv(DATA_PATH) 

for i in range(len(data)):
    emailSender.send(data[EMAIL_HEADER][i], data[NAME_HEADER][i], data[LINK_HEADER][i])

