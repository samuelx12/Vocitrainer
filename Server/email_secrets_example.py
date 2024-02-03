"""
email-secrets.py
Um die Bestätigunsemails zu versenden, braucht der Server zugang zu einem E-Mail Konto.
Dessen Anmeldedaten müssen hier eingetragen werden.
"""
# Login
SMTP_USERNAME = "info@example.com"
SMTP_PASSWORT = "super_secret_123"

# Server
SMTP_URL = "smtp.example.com"
SMTP_PORT = "465"

# Absender
ABSENDER = SMTP_USERNAME  # Der Absender sollte der E-Mail entsprechen, ansonsten könnten die E-Mails im Spam landen.
