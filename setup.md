🧠 Company Reputation Tracker — Setup Guide

This guide walks you through setting up the Company Reputation Tracker powered by CrewAI, equipped with agent-based scraping, sentiment analysis, SQLite data persistence, and dashboard reporting.

✅ 1. Environment Setup

🔧 Create and activate Conda environment (Python 3.10)

conda create -n crew python=3.10 -y
conda activate crew

🧠 Create and activate a virtual environment (Windows)

python -m venv .venv
.venv\Scripts\activate

⚠️ You should always activate .venv inside your conda environment to isolate project dependencies cleanly.

📆 2. Install Required Packages

✨ Install CrewAI and all tools

pip install "crewai[tools]"

🛠️ Optional: Ensure scraping tools are available

pip install selenium webdriver-manager

🔐 3. Set OpenAI API Key

🧪 Option A: Temporarily in terminal (Windows)

set OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

🧪 Option B: Store securely in a .env file

OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

Then use this snippet in your code to load it:

from dotenv import load_dotenv
load_dotenv()

📃️ 4. SQLite Integration (optional but recommended)

If you plan to persist data and visualize trends:

pip install sqlite-utils pandas sqlalchemy

You can inspect your DB using:

sqlite-utils data/mentions.db tables

🚀 5. Run the Agentic System

Run with default flow

crewai run

Optional: Run without re-creating virtualenv

uv run run_crew

✅ Summary

Component

Command / Tip

Conda Env

conda create -n crew python=3.10 -y

Virtual Env

python -m venv .venv && .venv\Scripts\activate

Install CrewAI

pip install "crewai[tools]"

Add API Key

set OPENAI_API_KEY=... or .env file

Run Crew

crewai run

SQLite Utils

pip install sqlite-utils pandas sqlalchemy

📁 Project Folder Example

company_reputation_tracker/
│
├── .venv/                      # Local virtualenv
├── agents.yaml                 # CrewAI agent roles
├── tasks.yaml                  # Task definitions
├── crew.py                     # Crew initialization script
├── main.py                     # Optional main entrypoint
├── database/mentions.db        # SQLite database
├── .env                        # OpenAI key
├── README.md                   # You're here
└── ...

