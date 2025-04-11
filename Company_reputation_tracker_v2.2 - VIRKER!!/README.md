# Company Reputation Tracker

A Dash-powered application that tracks company mentions from news sources, analyzes sentiment, and presents insights through an interactive dashboard.

## Features

- ✅ Input company names and aliases
- ✅ Fetch mentions from NewsAPI
- ✅ Analyze sentiment with TextBlob
- ✅ Store results in SQLite database
- ✅ Display insights in a Dash dashboard
- ✅ Automatic daily updates via GitHub Actions

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
```

### 2. Set Up API Keys

Create a `.env` file in the project root with:

```
NEWSAPI_KEY=your_newsapi_key_here
```

### 3. Initialize the Database

```bash
python db.py
```

### 4. Launch the Dashboard

```bash
python dashboard.py
```

This will start the Dash server, and you can access the dashboard at http://localhost:8050 in your browser.

## Using GitHub Actions for Automated Updates

This application uses GitHub Actions to automatically run the reputation tracking pipeline every day at 6:00 AM UTC.

### Setting Up GitHub Actions

1. Fork or push this repository to GitHub
2. Add your NewsAPI key as a repository secret:
   - Go to your repository → Settings → Secrets and variables → Actions
   - Add a new repository secret named `NEWSAPI_KEY` with your API key

The workflow will:
- Run automatically every day at 6:00 AM UTC
- Fetch and analyze new mentions for all companies
- Update the database and push changes back to the repository
- Save run reports as artifacts

### Manual Trigger

You can also manually trigger the workflow:
1. Go to your repository → Actions → "Daily Company Reputation Tracker"
2. Click "Run workflow"

## Command Line Usage

```bash
# Add a new company
python runner.py --add --name "Company Name" --aliases "Alias1,Alias2"

# Process a specific company
python runner.py --company 1

# List all companies
python runner.py

# Run a manual pipeline update for all companies
python runner.py --all
```

## Project Structure

```
company_tracker/
├── api_client.py         # NewsAPI client and TextBlob sentiment analysis
├── dashboard.py          # Dash dashboard interface
├── db.py                 # SQLite database models and operations
├── runner.py             # Main execution script
├── .github/
│   └── workflows/
│       └── daily_tracker.yml  # GitHub Actions workflow
├── requirements.txt
└── README.md
```

## Using the Dashboard

The Dash dashboard provides several features:

1. **Company Selection**: Choose from existing companies to view their reputation data
2. **Real-time Updates**: Click "Update Mentions Now" to fetch the latest mentions
3. **Add New Companies**: Easily add new companies and their aliases
4. **Sentiment Analysis**: See sentiment distribution across mentions
5. **Recent Mentions**: View the most recent mentions with sentiment highlighting
6. **Filtered Views**: Filter mentions by sentiment and time period
7. **Sortable Table**: Sort and filter the mentions table as needed