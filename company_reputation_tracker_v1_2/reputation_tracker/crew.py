# Import from the installed package, not local directory
import sys
import os

# Add parent dir to path to find the installed crewai package
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from crewai_tools import ScrapeWebsiteTool
from crewai_tools import ScrapeElementFromWebsiteTool
from crewai_tools import NL2SQLTool

@CrewBase
class IsYourReputationTrackerPartOfCrewAutomationCrew():
    """IsYourReputationTrackerPartOfCrewAutomation crew"""

    @agent
    def onboarding_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['onboarding_expert'],
            tools=[],
        )

    @agent
    def news_scraping_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['news_scraping_specialist'],
            tools=[ScrapeWebsiteTool(), ScrapeElementFromWebsiteTool()],
        )

    @agent
    def data_cleaning_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['data_cleaning_analyst'],
            tools=[],
        )

    @agent
    def sentiment_analysis_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['sentiment_analysis_expert'],
            tools=[],
        )

    @agent
    def sqlite_integration_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['sqlite_integration_specialist'],
            tools=[NL2SQLTool()],
        )

    @agent
    def dashboard_reporting_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['dashboard_reporting_specialist'],
            tools=[],
        )


    @task
    def onboarding_task_1(self) -> Task:
        return Task(
            config=self.tasks_config['onboarding_task_1'],
            tools=[],
        )

    @task
    def news_scraping_task(self) -> Task:
        return Task(
            config=self.tasks_config['news_scraping_task'],
            tools=[ScrapeWebsiteTool(), ScrapeElementFromWebsiteTool()],
        )

    @task
    def cleaning_task(self) -> Task:
        return Task(
            config=self.tasks_config['cleaning_task'],
            tools=[],
        )

    @task
    def sentiment_task(self) -> Task:
        return Task(
            config=self.tasks_config['sentiment_task'],
            tools=[],
        )

    @task
    def sqlite_task(self) -> Task:
        return Task(
            config=self.tasks_config['sqlite_task'],
            tools=[NL2SQLTool()],
        )

    @task
    def dashboard_task(self) -> Task:
        return Task(
            config=self.tasks_config['dashboard_task'],
            tools=[],
        )


    @crew
    def crew(self) -> Crew:
        """Creates the IsYourReputationTrackerPartOfCrewAutomation crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
