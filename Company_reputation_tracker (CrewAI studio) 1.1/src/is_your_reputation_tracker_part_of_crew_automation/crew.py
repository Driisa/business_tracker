from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool
from crewai_tools import SeleniumScrapingTool
from crewai_tools import ScrapeElementFromWebsiteTool

@CrewBase
class IsYourReputationTrackerPartOfCrewAutomationCrew():
    """IsYourReputationTrackerPartOfCrewAutomation crew"""

    @agent
    def onboarding_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['onboarding_agent'],
            tools=[],
        )

    @agent
    def web_scraping_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['web_scraping_specialist'],
            tools=[ScrapeWebsiteTool(), SeleniumScrapingTool(), ScrapeElementFromWebsiteTool()],
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
    def sqlite_integration_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['sqlite_integration_analyst'],
            tools=[],
        )

    @agent
    def dashboard_reporting_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['dashboard_reporting_specialist'],
            tools=[],
        )


    @task
    def onboarding_task(self) -> Task:
        return Task(
            config=self.tasks_config['onboarding_task'],
            tools=[],
        )

    @task
    def scraping_task(self) -> Task:
        return Task(
            config=self.tasks_config['scraping_task'],
            tools=[ScrapeWebsiteTool(), SeleniumScrapingTool(), ScrapeElementFromWebsiteTool()],
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
    def sqlite_integration_task(self) -> Task:
        return Task(
            config=self.tasks_config['sqlite_integration_task'],
            tools=[],
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
