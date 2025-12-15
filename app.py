import sys
import signal
import os
import threading

# --- 1. STREAMLIT THREAD FIX (Crucial for "ValueError: signal only works in main thread") ---
# This "monkey patches" the signal library. 
# If CrewAI tries to use signals in a background thread, we just ignore it.
original_signal = signal.signal

def thread_safe_signal(signum, handler):
    if threading.current_thread() is threading.main_thread():
        return original_signal(signum, handler)
    # If we are in a background thread (Streamlit), do nothing and don't crash
    return None

signal.signal = thread_safe_signal
# -----------------------------------------------------------------------------------------

# --- 2. WINDOWS FIX (Crucial for "AttributeError: SIGHUP") ---
if sys.platform.startswith('win'):
    missing_signals = [
        'SIGHUP', 'SIGQUIT', 'SIGTSTP', 'SIGCONT', 'SIGUSR1', 'SIGUSR2', 
        'SIGWINCH', 'SIGALRM', 'SIGPIPE', 'SIGTTIN', 'SIGTTOU', 'SIGVTALRM', 'SIGPROF'
    ]
    for sig in missing_signals:
        if not hasattr(signal, sig):
            setattr(signal, sig, 1)
# -----------------------------------------------------------

# --- 3. IMPORTS (Must be AFTER the fixes above) ---
import streamlit as st
from crewai import Crew
from agents import TripAgents
from tasks import TripTasks

# --- 4. STREAMLIT UI CONFIG ---
st.set_page_config(page_title="AI Trip Planner", page_icon="✈️", layout="wide")

st.markdown("""
<style>
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }
    .report-view {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #d6d6d6;
        font-family: monospace;
        white-space: pre-wrap; /* Keeps formatting */
    }
</style>
""", unsafe_allow_html=True)

# --- 5. SIDEBAR ---
with st.sidebar:
    st.title("✈️ Plan Your Trip")
    origin = st.text_input("From where?", "Nashik")
    cities = st.text_input("Destination?", "Goa")
    date_range = st.text_input("When?", "Next Week")
    interests = st.text_area("Interests?", "Beaches, Seafood, History")
    
    st.markdown("---")
    
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        api_key = st.text_input("Enter Groq API Key", type="password")
        if api_key:
            os.environ["GROQ_API_KEY"] = api_key

    run_btn = st.button("Generate Itinerary")

# --- 6. MAIN APP LOGIC ---
st.title("Agentic AI Trip Planner")
st.caption("Powered by CrewAI & Groq Llama 3.1")

if run_btn:
    if not os.environ.get("GROQ_API_KEY"):
        st.error("Please enter a Groq API Key to continue.")
    else:
        with st.spinner("🤖 Agents are researching & planning... (This takes 1-2 mins)"):
            try:
                # Initialize Agents/Tasks
                agents = TripAgents()
                tasks = TripTasks()

                city_selector = agents.city_selection_agent()
                local_expert = agents.local_expert()
                travel_concierge = agents.travel_concierge()

                identify = tasks.identify_task(city_selector, origin, cities, interests, date_range)
                gather = tasks.gather_task(local_expert, origin, interests, date_range)
                plan = tasks.plan_task(travel_concierge, origin, interests, date_range)

                # Create Crew with Rate Limits
                crew = Crew(
                    agents=[city_selector, local_expert, travel_concierge],
                    tasks=[identify, gather, plan],
                    verbose=True,
                    max_rpm=2 # Keeps us safe from Rate Limits
                )

                # Run!
                result = crew.kickoff()

                # Display Output
                st.success("Trip successfully planned!")
                st.markdown("### 🗺️ Your Itinerary")
                st.markdown(result)
                
                # Download Button
                st.download_button(
                    label="Download Itinerary",
                    data=str(result),
                    file_name="trip_plan.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")