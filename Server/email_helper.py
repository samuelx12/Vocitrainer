"""
email_helper.py
Helperfunktion für den Server um die Bestätigungsemail zu versenden.
"""

import smtplib
from email.mime.text import MIMEText
from email_konfiguration import SMTP_PASSWORT, SMTP_USERNAME, ABSENDER, SMTP_URL, SMTP_PORT


def email_senden(betreff: str, body: str, empfaenger: list) -> bool:
    """
    Diese Funktion sendet eine E-Mail über den in "email_konfiguration.py" beschriebenen E-Mail Account.
    :return bool Erfolg
    """

    msg = MIMEText(body)
    msg['Subject'] = betreff
    msg['From'] = "vocitrainer@barmet.ch"
    msg['To'] = ', '.join(empfaenger)

    try:
        with smtplib.SMTP_SSL(SMTP_URL, SMTP_PORT) as verbindung:
            verbindung.login(SMTP_USERNAME, SMTP_PASSWORT)
            verbindung.sendmail(ABSENDER, empfaenger, msg.as_string())
        return True
    except:
        # Beim Senden ist ein Fehler aufgetreten
        return False