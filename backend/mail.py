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
        id_list = id_list[::-1]

        page = int(page)
        i = (page - 1) * self.limit
        count = 0
        while (i < len(id_list) and count < self.limit):
            status, data = mail.fetch(str.encode(str(int(id_list[i]))), '(RFC822)')
            
            for response_part in data:
                if isinstance(response_part, tuple):
                    sign = False
                    
                    msg = email.message_from_string(codecs.decode(response_part[1],'utf-8'))
                    email_subject = msg['subject']
                    email_body = get_mail_body(msg)
                    email_from = msg['from']

                    type_email = email_subject.split(" - ")
                    if (type_email[0] == "ENC" and encrypt_key != "" and encrypt_mode != ""):
                        email_body = email_body.rstrip("\r\n")
                        email_body = email_body.replace("\r\n", "\n")
                        email_body = feistel.decrypt(encrypt_key, email_body, encrypt_mode)

                    elif (type_email[0] == "DSENC" and encrypt_key != "" and encrypt_mode != ""):
                        email_body_list = email_body.split("--BEGIN SIGNATURE SIGN--\r\n")

                        message_body = email_body_list[0]
                        message_body = message_body.rstrip("\r\n")
                        message_body = message_body.replace("\r\n", "\n")
                        message_body = feistel.decrypt(encrypt_key, message_body, encrypt_mode)

                        email_body = message_body + ("\n--BEGIN SIGNATURE SIGN--\n")  + email_body_list[1]
                    
                    if (type_email[0] == "DS" or type_email[0] == "DSENC"):
                        sign = True

                    obj = {}
                    obj["id"] = str(int(id_list[i]))
                    obj["from"] = email_from
                    obj["subject"] = email_subject
                    obj["body"] = email_body
                    obj["signature"] = sign

                    output.append(obj)

            i += 1
            count += 1

        return output
    
    def inbox_by_id(self, message_id):
        mail = imaplib.IMAP4_SSL(self.imap)
        mail.login(self.email, self.password)
        mail.select('"inbox"')

        status, data = mail.fetch(str.encode(str(int(message_id))), '(RFC822)')

        obj = {}
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(codecs.decode(response_part[1],'utf-8'))
                email_subject = msg['subject']
                email_body = get_mail_body(msg)
                email_from = msg['from']

                type_email = email_subject.split(" - ")
                
                if (type_email[0] == "DS" or type_email[0] == "DSENC"):
                    email_body_list = email_body.split("--BEGIN SIGNATURE SIGN--\r\n")

                    message_body = email_body_list[0]
                    message_body = message_body.rstrip("\r\n")
                    message_body = message_body.replace("\r\n", "\n")

                    signature_body = email_body_list[1]
                    signature_body = signature_body.split("\n--END SIGNATURE SIGN--")[0]
                    
                    t1, t2 = signature_body.split(';')
                    print(t1,t2)
                    t1 = int(t1).to_bytes(max(8, (int(t1).bit_length() + 7) // 8), "little")
                    t2 = int(t2).to_bytes(max(8, (int(t2).bit_length() + 7) // 8), "little")

                    signature_tuple = (bytes(t1), bytes(t2))

                obj["id"] = str(int(message_id))
                obj["from"] = email_from
                obj["subject"] = email_subject
                obj["body"] = email_body
                obj["originalMessage"] = message_body
                obj["signatureTuple"] = signature_tuple

        return obj

    def sent(self, page=1, encrypt_key="", encrypt_mode=""):
        output = []
        
        mail = imaplib.IMAP4_SSL(self.imap)
        mail.login(self.email, self.password)
        mail.select('"[Gmail]/Sent Mail"')

        status, data = mail.search(None, 'ALL')
        mail_ids = data[0]
        id_list = mail_ids.split()
        id_list = id_list[::-1]

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