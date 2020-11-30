import smtplib
import os
from dotenv import load_dotenv

def send(to, subject, message):
    load_dotenv()
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")

    print(email, password)
    
    try:
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login(email,password)
        sub = "Subject: " + subject + "\n\n" + message
        mail.sendmail(email,to,sub.encode('utf-8'))
        mail.quit()
        print("success")
        return True
    except Exception as e:
        print("unsuccess" + e)
        return False