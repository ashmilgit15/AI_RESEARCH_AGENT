from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from research_agent import agent,create_pdf,AIMessage,ToolMessage,HumanMessage

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static",StaticFiles(directory="static"),name="static")

@app.get("/")
def home(request:Request):
    return templates.TemplateResponse(request=request,name="index.html")


@app.post("/research")
def research(topic:str):
        final_report = None
        for event in agent.stream(
        {"messages": [HumanMessage(content=f"You are an AI research Agent called Trau created by Ashmil. Research this topic thoroughly and create a detailed and comprehensive report: {topic}")]},
        stream_mode="updates"
    ):
        
            for node,data in event.items():
                messages = data.get("messages",[])

                for message in messages:
                    if hasattr(message,"tool_calls") and message.tool_calls:
                        for tool_call in message.tool_calls:
                            query = tool_call.get("args",{}).get("query","")
                            print(f"Searching: {query}")

                    elif isinstance(message,ToolMessage):
                        print(f"fetched results for: {message.name}")


                    elif isinstance(message,AIMessage):
                        print(f"\nReports:\n{message.content}")
                        final_report = message.content


        if final_report:
            create_pdf(final_report,f"{topic}.pdf")    
            return {"message":"report generated succesfully"}           