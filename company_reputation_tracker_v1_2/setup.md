✅ 1. Prerequisites
Before running the system, ensure the following are installed on your machine:

🛠️ Install:
Python 3.10+: Download from python.org

Git: Download from git-scm.com

A virtual environment tool (like venv, which comes with Python)

📦 2. Set Up the Project
Assuming you've already extracted the zip folder:

🔁 Open a terminal (Command Prompt / PowerShell) and run:
bash
Kopiér
Rediger
cd path\to\reputation_tracker_extracted
python -m venv venv
venv\Scripts\activate
Replace path\to\reputation_tracker_extracted with your actual path, like C:\Users\YourName\Downloads\reputation_tracker_extracted

📥 3. Install Dependencies
bash
Kopiér
Rediger
pip install -U pip
pip install -e .
This uses pyproject.toml to install the project in editable mode (like a dev setup).

⚙️ 4. Configure Your Agents
Open these files and customize as needed:

src/.../config/agents.yaml: defines the agents and their LLM settings

src/.../config/tasks.yaml: defines what the agents do

If you're using OpenAI API, make sure to set your API key in the environment:

bash
Kopiér
Rediger
$env:OPENAI_API_KEY="sk-..."  # PowerShell
# or
set OPENAI_API_KEY=sk-...     # CMD
🚀 5. Run the Agentic System
bash
Kopiér
Rediger
cd src\is_your_reputation_tracker_part_of_crew_automation
python main.py
This will kick off the CrewAI process as defined in crew.py and main.py.

🧠 Extra Tips
To debug or enhance tools: edit custom_tool.py

To change knowledge base: update knowledge/user_preference.txt

To log what's happening: add print() or logging to crew.py