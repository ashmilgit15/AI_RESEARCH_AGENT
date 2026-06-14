# TRAU - RESEARCH AGENT

i built this becaude i dont like jumping into multiple tabs to do a deep research , it also downloads the report.pdf automatically

## Setup

```bash
git clone https://github.com/ashmilgit15/AI_RESEARCH_AGENT.git
cd AI_RESEARCH_AGENT
uv sync
cp .env.example .env  # add your API keys
uvicorn main:app --reload
```

Open http://localhost:8000, type a topic, hit Generate.


## CREDITS

* [Tavily](app.tavily.com)
* [Hackclub-api-key](ai.hackclub.com)
* [Langchain](www.langchain.com)
* [Fastapi](fastapi.tiangolo.com)
