# import smtplib
# import os
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()

# def send_email(to_email: str, subject: str, body_html: str):
#     EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
#     EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

#     if not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
#         raise ValueError("Missing EMAIL_HOST_USER or EMAIL_HOST_PASSWORD in environment variables.")

#     msg = MIMEMultipart()
#     msg["From"] = EMAIL_HOST_USER
#     msg["To"] = to_email
#     msg["Subject"] = subject
#     msg.attach(MIMEText(body_html, "html"))

#     try:
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:
#             server.starttls()
#             server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
#             server.sendmail(EMAIL_HOST_USER, to_email, msg.as_string())
#     except Exception as e:
#         print("Failed to send email:", e)


# app/EMail/email_service.py

import smtplib
import os
from typing import List, Union
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

def send_email(subject: str, recipients: Union[str, List[str]], body_html: str):
    if isinstance(recipients, str):
        recipients = [recipients]

    if not EMAIL_HOST_USER or not EMAIL_HOST_PASSWORD:
        raise ValueError("Missing EMAIL_HOST_USER or EMAIL_HOST_PASSWORD")

    msg = MIMEMultipart()
    msg["From"] = EMAIL_HOST_USER
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.attach(MIMEText(body_html, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.sendmail(EMAIL_HOST_USER, recipients, msg.as_string())
    except Exception as e:
        print("Failed to send email:", e)
