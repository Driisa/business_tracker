from crewai import Agent
from tools.tools import vader_tool, gpt_sentiment_tool

# SentimentAgent
sentiment_agent = Agent(
    role="SentimentAnalyzer",
    goal="Score the sentiment of company mentions and flag potential crises.",
    backstory="You are a linguistic analyst trained to detect subtle sentiment changes in text.",
    tools=[vader_tool, gpt_sentiment_tool],
    verbose=True
)