from crewai import Agent
from tools.tools import trend_detection_tool

# TrendAnalyzerAgent
trend_analyzer_agent = Agent(
    role="TrendAnalyzer",
    goal="Detect spikes, influencer mentions, and major shifts in reputation over time.",
    backstory="You are responsible for spotting trends and anomalies in how companies are talked about.",
    tools=[trend_detection_tool],
    verbose=True
)