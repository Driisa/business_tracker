from crewai import Crew, Agent
from agents.mention_fetcher import mention_fetcher_agent
from agents.sentiment_agent import sentiment_agent
from agents.review_agent import review_aggregator_agent
from agents.trend_agent import trend_analyzer_agent
from tasks import (
    fetch_mentions_task,
    analyze_sentiment_task,
    aggregate_reviews_task,
    analyze_trends_task
)

company_crew = Crew(
    name="Acme Reputation Crew",
    agents=[
        mention_fetcher_agent,
        sentiment_agent,
        review_aggregator_agent,
        trend_analyzer_agent
    ],
    tasks=[
        fetch_mentions_task,
        analyze_sentiment_task,
        aggregate_reviews_task,
        analyze_trends_task
    ],
    process="sequential"
)

def run_company_crew():
    company_crew.run()