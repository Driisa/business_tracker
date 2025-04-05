# --- main.py (Entrypoint) ---

from dotenv import load_dotenv
load_dotenv()
import os
from tools.crew import run_company_crew

if __name__ == "__main__":
    company_name = os.getenv("COMPANY_NAME", "Acme Corp")
    print(f"\n🚀 Running CrewAI Reputation Tracker for: {company_name}\n")
    run_company_crew()
    print("\n✅ Crew run completed. Dashboard and reports will reflect the updates.\n")
    