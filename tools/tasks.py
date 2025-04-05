# --- tasks.py (Task Definitions) ---

from crewai import Task
from agents.mention_fetcher import mention_fetcher_agent
from agents.sentiment_agent import sentiment_agent
from agents.review_agent import review_aggregator_agent
from agents.trend_agent import trend_analyzer_agent

fetch_mentions_task = Task(
    description="Fetch all relevant public mentions of {{ company.name }} using provided tools.",
    agent=mention_fetcher_agent
)

analyze_sentiment_task = Task(
    description="Analyze sentiment for all collected mentions of {{ company.name }}. Classify as positive, neutral, or negative.",
    agent=sentiment_agent
)

aggregate_reviews_task = Task(
    description="Gather and summarize recent reviews of {{ company.name }} from major platforms.",
    agent=review_aggregator_agent
)

analyze_trends_task = Task(
    description="Analyze trends and patterns in mentions and reviews of {{ company.name }}. Flag spikes or anomalies.",
    agent=trend_analyzer_agent
)