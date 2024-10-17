import os
from dotenv import load_dotenv
from smtplib import SMTP

load_dotenv()

MY_EMAIL = os.environ['SENDER_EMAIL']
MY_PASSWORD = os.environ['SENDER_PASSWORD']


def send_email(message, to_email):
    mail_action = SMTP("smtp.gmail.com",587)
    mail_action.starttls()
    mail_action.login(
        user=MY_EMAIL,
        password=MY_PASSWORD
    )
    mail_action.sendmail(
        from_addr=MY_EMAIL,
        to_addrs=to_email,
        msg=message.encode(encoding="utf8")
    )


