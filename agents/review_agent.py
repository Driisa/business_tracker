from crewai import Agent
from tools.tools import trustpilot_tool, glassdoor_tool

# ReviewAggregatorAgent
review_aggregator_agent = Agent(
    role="ReviewAggregator",
    goal="Collect and summarize public reviews from Trustpilot, Glassdoor, G2, and more.",
    backstory="You are trained in scraping and interpreting review-based feedback for brands.",
    tools=[trustpilot_tool, glassdoor_tool],
    verbose=True
)