######################################
#          Email Sender v2           #
#                                    #
#     Developed By DarkKnight        #
######################################

import pandas as pd
import yagmail


SENDER_EMAIL = 'YOUR_EMAIL'
SENDER_PASS = 'YOUR_PASSWORD'
SUBJECT = 'YOUR SUBJECT LIE HERE'
TEMPLATE_PATH = './email-template.txt'
ATTACHMENTS_BASE_PATH = './attachments/'
DATA_PATH = './data.csv'
NAME_HEADER = 'Name'
EMAIL_HEADER = 'Email'
LINK_HEADER = 'Link'
ATTACHMENT_EXTENSION = '.png'


class EmailSender:
    def __init__(self, sender_email, sender_pass):
        self.sender_email = sender_email

        try:
            self.server = yagmail.SMTP(sender_email, sender_pass)
        except Exception as e:
            print("***Can't login to this gmail***")
            print(e)

        self.getTemplate(TEMPLATE_PATH)

    def __del__(self):
        self.server.close()

    def getTemplate(self, template_path):
        with open(template_path, 'r') as file:
            self.template = ''.join(file.readlines())

    def getEmailText(self, name, link):
        return self.template.replace('NAME', name).replace('LINK', link)

    def getAttachmentFileName(self, name):
        return ATTACHMENTS_BASE_PATH + name + ATTACHMENT_EXTENSION

    def send(self, to, name, link):
        try:
            self.server.send(
                to=to,
                subject=SUBJECT,
                contents=self.getEmailText(name, link),
                attachments=self.getAttachmentFileName(name)
            )
            print(f'[+] Successfully sent to: {name}')
        except Exception as e:
            print(f'[-] Failed sent to: {name}\n cause: {e}\n')


emailSender = EmailSender(SENDER_EMAIL, SENDER_PASS)

data = pd.read_csv(DATA_PATH)

for i in range(len(data)):
    emailSender.send(
        data[EMAIL_HEADER][i],
        data[NAME_HEADER][i], 
        data[LINK_HEADER][i]
    )
