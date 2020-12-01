import codecs
import email
import smtplib
import imaplib
import os
from dotenv import load_dotenv
import algorithms.feistel as feistel

def get_mpart(mail):
    maintype = mail.get_content_maintype()
    if maintype == 'multipart':
        for part in mail.get_payload():
            if part.get_content_maintype() == 'text':
                return part.get_payload()
        return ""
    elif maintype == 'text':
        return mail.get_payload()


def get_mail_body(mail):
    if mail.is_multipart():
        body = get_mpart(mail)
    else:
        body = mail.get_payload()
    return body

class Mail:
    def __init__(self):
        load_dotenv()
        self.email = os.getenv("EMAIL")
        self.password = os.getenv("PASSWORD")
        self.smtp = "smtp.gmail.com"
        self.smtp_port = 587
        self.imap = "imap.gmail.com"
        self.imap_port = 993
        self.limit = 10

    def send(self, to, subject, message):
        mail = smtplib.SMTP(self.smtp, 587)
        mail.ehlo()
        mail.starttls()
        mail.login(self.email, self.password)
        
        data = "Subject: " + subject + "\n\n" + message
        mail.sendmail(self.email, [to], data.encode('utf-8'))
        mail.quit()

    def inbox(self, page=1, encrypt_key="", encrypt_mode=""):
        output = []
        
        mail = imaplib.IMAP4_SSL(self.imap)
        mail.login(self.email, self.password)
        mail.select('"inbox"')

        status, data = mail.search(None, 'ALL')
        mail_ids = data[0]
        id_list = mail_ids.split()

        page = int(page)
        i = (page - 1) * self.limit
        count = 0
        while (i < len(id_list) and count < self.limit):
            status, data = mail.fetch(str.encode(str(int(id_list[i]))), '(RFC822)')
            
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(codecs.decode(response_part[1],'utf-8'))
                    email_subject = msg['subject']
                    email_body = get_mail_body(msg)
                    email_from = msg['from']

                    type_email = email_subject.split(" - ")
                    if (type_email[0] == "ENC" and encrypt_key != "" and encrypt_mode != ""):
                        email_body = email_body.rstrip("\r\n")
                        email_body = email_body.replace("\r\n", "\n")
                        email_body = feistel.decrypt(encrypt_key, email_body, encrypt_mode)

                    obj = {}
                    obj["id"] = str(int(id_list[i]))
                    obj["from"] = email_from
                    obj["subject"] = email_subject
                    obj["body"] = email_body

                    output.append(obj)

            i += 1
            count += 1

        return output

    def sent(self, page=1, encrypt_key="", encrypt_mode=""):
        output = []
        
        mail = imaplib.IMAP4_SSL(self.imap)
        mail.login(self.email, self.password)
        mail.select('"[Gmail]/Sent Mail"')

        status, data = mail.search(None, 'ALL')
        mail_ids = data[0]
        id_list = mail_ids.split()

        page = int(page)
        i = (page - 1) * self.limit
        count = 0
        while (i < len(id_list) and count < self.limit):
            status, data = mail.fetch(str.encode(str(int(id_list[i]))), '(RFC822)')
            
            for response_part in data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_string(codecs.decode(response_part[1],'utf-8'))
                    email_subject = msg['subject']
                    email_body = get_mail_body(msg)
                    email_to = msg['bcc']

                    type_email = email_subject.split(" - ")
                    if (type_email[0] == "ENC" and encrypt_key != "" and encrypt_mode != ""):
                        email_body = email_body.rstrip("\r\n")
                        email_body = email_body.replace("\r\n", "\n")
                        email_body = feistel.decrypt(encrypt_key, email_body, encrypt_mode)

                    obj = {}
                    obj["id"] = str(int(id_list[i]))
                    obj["to"] = email_to
                    obj["subject"] = email_subject
                    obj["body"] = email_body

                    output.append(obj)

            i += 1
            count += 1

        return output