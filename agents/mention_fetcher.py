from crewai import Agent
from tools.tools import NewsApiTool, RedditTool, XTool

mention_fetcher_agent = Agent(
    role="MentionFetcher",
    goal="Find all public mentions of a given company from news, social, and forums.",
    backstory="You specialize in sourcing timely and relevant company mentions across the web.",
    tools=[NewsApiTool(), RedditTool(), XTool()],
    verbose=True
)