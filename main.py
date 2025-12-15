import os
import sys
import signal

# --- UNIVERSAL WINDOWS FIX ---
if sys.platform.startswith('win'):
    missing_signals = [
        'SIGHUP', 'SIGQUIT', 'SIGTSTP', 'SIGCONT', 'SIGUSR1', 'SIGUSR2', 
        'SIGWINCH', 'SIGALRM', 'SIGPIPE', 'SIGTTIN', 'SIGTTOU', 'SIGVTALRM', 'SIGPROF'
    ]
    for sig in missing_signals:
        if not hasattr(signal, sig):
            setattr(signal, sig, 1)
# -----------------------------

from crewai import Crew
from textwrap import dedent
from agents import TripAgents
from tasks import TripTasks
from dotenv import load_dotenv

load_dotenv()

class TripCrew:

  def __init__(self, origin, cities, date_range, interests):
    self.cities = cities
    self.origin = origin
    self.interests = interests
    self.date_range = date_range

  def run(self):
    agents = TripAgents()
    tasks = TripTasks()

    city_selector_agent = agents.city_selection_agent()
    local_expert_agent = agents.local_expert()
    travel_concierge_agent = agents.travel_concierge()

    identify_task = tasks.identify_task(
      city_selector_agent,
      self.origin,
      self.cities,
      self.interests,
      self.date_range
    )
    gather_task = tasks.gather_task(
      local_expert_agent,
      self.origin,
      self.interests,
      self.date_range
    )
    plan_task = tasks.plan_task(
      travel_concierge_agent, 
      self.origin,
      self.interests,
      self.date_range
    )

    crew = Crew(
      agents=[
        city_selector_agent, local_expert_agent, travel_concierge_agent
      ],
      tasks=[identify_task, gather_task, plan_task],
      verbose=True,
      # --- FIX: Slow down to 2 requests per minute to stay free ---
      max_rpm=2
    )

    result = crew.kickoff()
    return result

if __name__ == "__main__":
  print("## Welcome to Trip Planner Crew (Groq Edition)")
  print('-------------------------------')
  
  if not os.environ.get("GROQ_API_KEY"):
      os.environ["GROQ_API_KEY"] = input("Please enter your GROQ_API_KEY: ")

  location = input(dedent("""From where will you be traveling from? """))
  cities = input(dedent("""What are the cities options you are interested in visiting? """))
  date_range = input(dedent("""What is the date range you are interested in traveling? """))
  interests = input(dedent("""What are some of your high level interests and hobbies? """))
   
  trip_crew = TripCrew(location, cities, date_range, interests)
  result = trip_crew.run()
  print("\n\n########################")
  print("## Here is you Trip Plan")
  print("########################\n")
  print(result)