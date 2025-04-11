Company Reputation Tracker
A Dash-powered application that tracks company mentions from news sources, analyzes sentiment using advanced AI models, and presents insights through an interactive dashboard.

Features
✅ Input company names and aliases
✅ Fetch mentions from NewsAPI
✅ Analyze sentiment with Hugging Face Transformers
✅ Store results in SQLite database
✅ Display insights in an interactive Dash dashboard
✅ Automatic daily updates via GitHub Actions
✅ Sentiment timeline visualization
✅ Advanced sentiment metrics
Quick Start
Easy Setup
Run the setup script to install dependencies and initialize the database:

bash
python setup.py
Manual Setup
Install Dependencies
bash
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
Set Up API Keys
Create a .env file in the project root with:

NEWSAPI_KEY=your_newsapi_key_here
Initialize the Database
bash
python db.py
Launch the Dashboard
bash
python dashboard.py
This will start the Dash server, and you can access the dashboard at http://localhost:8050 in your browser.

Using GitHub Actions for Automated Updates
This application uses GitHub Actions to automatically run the reputation tracking pipeline every day at 6:00 AM UTC.

Setting Up GitHub Actions
Fork or push this repository to GitHub
Add your NewsAPI key as a repository secret:
Go to your repository → Settings → Secrets and variables → Actions
Add a new repository secret named NEWSAPI_KEY with your API key
The workflow will:

Run automatically every day at 6:00 AM UTC
Fetch and analyze new mentions for all companies
Update the database and push changes back to the repository
Save run reports as artifacts
Manual Trigger
You can also manually trigger the workflow:

Go to your repository → Actions → "Daily Company Reputation Tracker"
Click "Run workflow"
Command Line Usage
bash
# Add a new company
python runner.py --add --name "Company Name" --aliases "Alias1,Alias2"

# Process a specific company
python runner.py --company 1

# List all companies
python runner.py

# Run a manual pipeline update for all companies
python runner.py --all
Advanced Sentiment Analysis
This application uses Hugging Face Transformers for state-of-the-art sentiment analysis:

Model: DistilBERT fine-tuned on SST-2 dataset
Scoring: Range from -1 (very negative) to 1 (very positive)
Classification: POSITIVE, NEUTRAL, NEGATIVE based on score thresholds
Timeline: Track sentiment changes over time with trend analysis
If Hugging Face dependencies cannot be installed on your system, the application will automatically fall back to TextBlob for basic sentiment analysis.

Project Structure
company_tracker/
├── api_client.py         # NewsAPI client and sentiment analysis
├── dashboard.py          # Dash dashboard interface
├── db.py                 # SQLite database models and operations
├── runner.py             # Main execution script
├── setup.py              # Setup script for easy installation
├── .github/
│   └── workflows/
│       └── daily_tracker.yml  # GitHub Actions workflow
├── requirements.txt
└── README.md
Dashboard Features
The Dash dashboard provides several features:

Company Management: Add and select companies to track
Sentiment Overview: Distribution of positive, negative, and neutral mentions
Sentiment Score: Average sentiment score with visual indicator
Sentiment Timeline: Track sentiment changes over time with trend line
Recent Mentions: View most recent mentions with sentiment highlighting
Filtered Views: Filter mentions by sentiment and time period
Sortable Table: Sort and filter the mentions table as needed
Troubleshooting
If you encounter issues installing the Hugging Face dependencies:

Try running python setup.py which will offer to install minimal dependencies
Or manually install the minimal requirements:
bash
pip install dash dash-bootstrap-components plotly sqlalchemy requests python-dotenv pandas
The application will automatically fall back to simpler sentiment analysis methods if advanced models are not available.

