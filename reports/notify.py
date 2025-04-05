# --- reports/notify.py (Email/Slack Delivery) ---

import os
import smtplib
from email.mime.text import MIMEText
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def send_email(recipient, subject, body):
    sender = os.getenv("SMTP_SENDER")
    password = os.getenv("SMTP_PASSWORD")
    smtp_server = os.getenv("SMTP_SERVER")
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient

    with smtplib.SMTP_SSL(smtp_server, 465) as server:
        server.login(sender, password)
        server.sendmail(sender, recipient, msg.as_string())

def send_slack_message(channel, text):
    slack_token = os.getenv("SLACK_API_TOKEN")
    client = WebClient(token=slack_token)
    try:
        client.chat_postMessage(channel=channel, text=text)
    except SlackApiError as e:
        print(f"Slack Error: {e.response['error']}")