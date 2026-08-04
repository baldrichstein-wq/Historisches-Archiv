import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

SMTP_SERVER = os.getenv("SMTP_SERVER", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "noreply@historisches-archiv.de")
WEBMASTER_EMAIL = "webmaster@32meininger.de"
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")

def send_email(to_email, subject, body):
    if not SMTP_SERVER or not SMTP_USER or not SMTP_PASSWORD:
        print("--- EMAIL MOCK ---")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(f"Body:\n{body}")
        print("------------------")
        return

    msg = MIMEMultipart()
    msg['From'] = FROM_EMAIL
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(FROM_EMAIL, to_email, text)
        server.quit()
        print(f"Email sent successfully to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {str(e)}")

def send_verification_email(user_email, token):
    verification_link = f"{FRONTEND_URL}/verify?token={token}"
    subject = "Bitte bestätige deine E-Mail-Adresse für das Historische Archiv"
    body = f"Hallo,\n\nvielen Dank für deine Registrierung.\nBitte klicke auf den folgenden Link, um deine E-Mail-Adresse zu bestätigen:\n\n{verification_link}\n\nDein Historisches Archiv Team."
    send_email(user_email, subject, body)

def send_admin_notification(new_user_email, new_user_username):
    subject = "Neue Registrierung im Historischen Archiv"
    body = f"Hallo Webmaster,\n\nes gibt eine neue Registrierung im Historischen Archiv.\n\nBenutzername: {new_user_username}\nE-Mail: {new_user_email}\nRolle (Standard): Gast\n\nViele Grüße,\nDein Historisches Archiv System."
    send_email(WEBMASTER_EMAIL, subject, body)
