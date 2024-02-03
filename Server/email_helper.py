"""
email_helper.py
Zuerst nur ein Test
"""

import smtplib
from email.mime.text import MIMEText
from email_secrets import SMTP_PASSWORT, SMTP_USERNAME, ABSENDER, SMTP_URL, SMTP_PORT

betreff = "Test für Vocitrainer EMail"
nachricht = "Das hier ist die Test-Nachricht:\nLorem Ipsum Dolor sit amet..."
empfaenger = [SMTP_USERNAME, "barm.samu.2018@ksz.edu-zg.ch"]


def email_senden(betreff: str, body: str, empfaenger: list):
    """

    :param betreff:
    :param body:
    :param absender:
    :param empfaenger:
    :param passwort:
    :return:
    """

    absender = SMTP_USERNAME

    msg = MIMEText(body)
    msg['Subject'] = betreff
    msg['From'] = "vocitrainer@barmet.ch"
    msg['To'] = ', '.join(empfaenger)

    with smtplib.SMTP_SSL(SMTP_URL, SMTP_PORT) as verbindung:
        verbindung.login(SMTP_USERNAME, SMTP_PASSWORT)
        verbindung.sendmail(absender, empfaenger, msg.as_string())

    print("Message sent!")


email_senden(betreff, nachricht, empfaenger)
