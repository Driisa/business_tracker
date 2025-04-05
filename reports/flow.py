# --- reports/flow.py (Prefect PDF & Notification Flow) ---

from dotenv import load_dotenv
load_dotenv()

from prefect import flow, task
from reports.generate_pdf import generate_pdf_report
from reports.notify import send_email, send_slack_message
import os

@task
def create_report(company_name: str, summary_text: str):
    return generate_pdf_report(company_name, summary_text)

@task
def notify_team(company_name: str, pdf_path: str):
    email = os.getenv("TEAM_EMAIL")
    subject = f"📄 Weekly Reputation Report - {company_name}"
    body = f"Your reputation report is ready: {pdf_path}"
    send_email(email, subject, body)
    send_slack_message("#reputation-updates", f"📣 {company_name}'s report ready: {pdf_path}")

@flow(name="Report and Notify")
def report_and_notify_flow():
    company_name = os.getenv("COMPANY_NAME", "Acme Corp")
    summary_text = f"Summary for {company_name}: All systems stable. Positive brand perception."
    pdf_path = create_report(company_name, summary_text)
    notify_team(company_name, pdf_path)

if __name__ == "__main__":
    report_and_notify_flow()