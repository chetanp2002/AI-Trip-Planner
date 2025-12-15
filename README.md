# TripCrew  

An intelligent travel planning application powered by **CrewAI**, **Groq (Llama 3.1)**, and **Streamlit**. This tool uses a team of autonomous AI agents to research, plan, and budget a complete 7-day travel itinerary based on your interests.  

## 🌟 Features  
- **Multi-Agent Architecture:** Three specialized agents (City Selector, Local Expert, Concierge) work in sequence.  
- **Live Internet Access:** Uses DuckDuckGo to fetch real-time flight prices and weather.  
- **Web Scraping:** Capable of reading travel blogs and official tourism websites.  
- **Budget Calculation:** Automatically estimates flight, hotel, and food costs.  
- **Rate Limit Handling:** Optimized with threading and **RPM** limits to run smoothly on Groq's Free Tier.  

## 🛠️ Tech Stack  
- **Framework:** CrewAI (Agent Orchestration)  
- ****LLM**:** Groq Llama 3.1 8B (Inference)  
- **Frontend:** Streamlit  
- **Tools:** LangChain Community, DuckDuckGo Search  
- **Language:** Python 3.10+  

## 🚀 Installation  

1. **Clone the repository:**  
    ```bash  
    git clone https://github.com/chetanp2002/TripCrew
    ```
    ```bash 
    cd TripCrew  
    ```  

2. **Create a Virtual Environment:**  
    ```bash  
    conda create -n venv python=3.10  
    ```
    ```bash
    conda activate venv/  
    ```  

3. **Install Dependencies:**  
    ```bash  
    pip install -r requirements.txt  
    ```  

4. **Set up Environment Variables:**  
    Create a `.env` file in the root directory:  
    ```env  
    GROQ_API_KEY=gsk_your_key_here  
    ```  

## ▶️ Usage  

Run the Streamlit application:  
```bash  
streamlit run app.py  
```
Open your browser to http://localhost:8501  

## 📂 Project Structure  
- app.py: Main entry point and UI logic.  

- agents.py: Defines the 3 AI Agents and their **LLM** configuration.  

- tasks.py: Defines the specific instructions for each agent.  

- trip_tools.py: Custom tools for searching, scraping, and calculating.  

## 🤝 Credits  
Built using the CrewAI framework and the Groq API.  