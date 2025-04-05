# --- scheduler.py (Prefect Scheduled Flow) ---

from dotenv import load_dotenv
load_dotenv()
from prefect import flow, task
from crew import run_company_crew
import os

@task
def run_agentic_workflow():
    company_name = os.getenv("COMPANY_NAME", "Acme Corp")
    print(f"[Prefect] Starting scheduled run for: {company_name}")
    run_company_crew()
    print("[Prefect] Workflow completed.")

@flow(name="Reputation Monitoring Scheduler")
def scheduled_reputation_monitor():
    run_agentic_workflow()

if __name__ == "__main__":
    scheduled_reputation_monitor()