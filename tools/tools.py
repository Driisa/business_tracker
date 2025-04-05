from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from typing import Type
import requests
import os

# ------------------ Mention Fetcher Tools ------------------

class NewsApiInput(BaseModel):
    company_name: str = Field(..., description="Company name to search for in NewsAPI")

class NewsApiTool(BaseTool):
    name: str = "NewsAPI Mention Search"
    description: str = "Fetches the latest news articles mentioning the given company using NewsAPI"
    args_schema: Type[BaseModel] = NewsApiInput

    def _run(self, company_name: str) -> str:
        api_key = os.getenv("NEWS_API_KEY")
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": company_name,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 10,
            "apiKey": api_key
        }
        response = requests.get(url, params=params)
        return str(response.json().get("articles", []))

class RedditTool(BaseTool):
    name: str = "Reddit Mention Search"
    description: str = "Simulates Reddit mentions for the given company"
    args_schema: Type[BaseModel] = NewsApiInput

    def _run(self, company_name: str) -> str:
        return f"[Reddit result for {company_name}]"

class XTool(BaseTool):
    name: str = "Twitter/X Scraper"
    description: str = "Simulates scraping Twitter/X for mentions"
    args_schema: Type[BaseModel] = NewsApiInput

    def _run(self, company_name: str) -> str:
        return f"[X/Twitter result for {company_name}]"

# ------------------ Sentiment Tools ------------------

class SentimentInput(BaseModel):
    text: str = Field(..., description="The text to analyze for sentiment")

class VaderSentimentTool(BaseTool):
    name: str = "VADER Sentiment Analyzer"
    description: str = "Analyzes sentiment using VADER"
    args_schema: Type[BaseModel] = SentimentInput

    def _run(self, text: str) -> str:
        # Simulate VADER sentiment analysis
        return "Positive (simulated VADER)"

class GptSentimentTool(BaseTool):
    name: str = "GPT Sentiment Analyzer"
    description: str = "Analyzes sentiment using a GPT-based method"
    args_schema: Type[BaseModel] = SentimentInput

    def _run(self, text: str) -> str:
        # Simulate GPT-based sentiment analysis
        return "Neutral (simulated GPT)"

# ✅ Instantiate tools so they can be imported elsewhere
vader_tool = VaderSentimentTool()
gpt_sentiment_tool = GptSentimentTool()
