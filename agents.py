import os
from crewai import Agent, LLM
from trip_tools import SearchTool, ScrapeTool, CalculatorTool

class TripAgents():
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        self.llm = LLM(
            model="groq/llama-3.1-8b-instant",
            api_key=api_key
        )

    def city_selection_agent(self):
        return Agent(
            role='City Selection Expert',
            goal='Select the best city based on weather, season, and prices',
            backstory='An expert in analyzing travel data to pick ideal destinations',
            tools=[SearchTool(), ScrapeTool()],
            llm=self.llm,
            verbose=True,
            max_iter=1  # <--- CHANGED TO 1 (Stops memory overflow)
        )

    def local_expert(self):
        return Agent(
            role='Local Expert at this city',
            goal='Provide the BEST insights about the selected city',
            backstory="""A knowledgeable local guide with extensive information
            about the city, it's attractions and customs""",
            tools=[SearchTool(), ScrapeTool()],
            llm=self.llm,
            verbose=True,
            max_iter=1  # <--- CHANGED TO 1
        )

    def travel_concierge(self):
        return Agent(
            role='Amazing Travel Concierge',
            goal="""Create the most amazing travel itineraries with budget and 
            packing suggestions for the city""",
            backstory="""Specialist in travel planning and logistics with 
            decades of experience""",
            tools=[
                SearchTool(), 
                ScrapeTool(), 
                CalculatorTool()
            ],
            llm=self.llm,
            verbose=True,
            max_iter=1  # <--- CHANGED TO 1
        )