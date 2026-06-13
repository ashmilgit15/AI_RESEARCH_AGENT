 # Trau — AI Research Agent                                                                                                                                                                       
                                                                                                                                                                                                     
    Give it a topic, get a proper research PDF. Pulls from multiple sources via Tavily,                                                                                                              
    compiles a structured report, and drops it straight into your downloads folder.                                                                                                                  
                                                                                                                                                                                                     
    Built this because I kept switching between 15 tabs whenever I needed to research something.                                                                                                     
                                                                                                                                                                                                     
    ## Stack                                                                                                                                                                                         
    - FastAPI + Uvicorn                                                                                                                                                                              
    - LangChain (ReAct agent)                                                                                                                                                                        
    - Tavily Search API                                                                                                                                                                              
    - WeasyPrint for PDF generation                                                                                                                                                                  
    - Kimi K2 via Hack Club's AI proxy                                                                                                                                                               
                                                                                                                                                                                                     
    ## Setup
  
    ```bash
    git clone https://github.com/ashmilgit15/AI_RESEARCH_AGENT.git
    cd AI_RESEARCH_AGENT
    uv sync
    cp .env.example .env  # add your API keys
    uvicorn main:app --reload
  
  Open http://localhost:8000, type a topic, hit Generate.


## CREDITS

* [Tavily](app.tavily.com)
* [Hackclub-api-key](ai.hackclub.com)
* [Langchain](www.langchain.com)
* [Fastapi](fastapi.tiangolo.com)
