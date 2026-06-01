from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage , AIMessage , ToolMessage
from fpdf import FPDF
import os
import re
load_dotenv()

tavily_api_key = os.getenv("TAVILY_API_KEY")
hackclub_api_key = os.getenv("HACKCLUB_API_KEY")

llm = ChatOpenAI(
    model="moonshotai/kimi-k2.6",
    api_key=hackclub_api_key,
    base_url = "https://ai.hackclub.com/proxy/v1"
)

search_tool = TavilySearch(
    max_results = 5,
    api_key = tavily_api_key,
)

llm_with_tools = llm.bind_tools([search_tool])

agent  =create_react_agent(
    model = llm,
    tools=[search_tool]
)
while True:

    

    topic = input("Enter research topic(or quit:'quit'): ")

    if topic.lower() == "quit":
        break

    print("Trau is Working.....")

    

    for event in agent.stream(
        {"messages": [HumanMessage(content=f"You are an AI research Agent called Trau created by Ashmil. Research this topic thoroughly and create a detailed and comprehensive report: {topic}")]},
        stream_mode="updates"
    ):
        
        for node,data in event.items():
            messages = data.get("messages",[])

            for message in messages:
                if hasattr(message,"tool_calls") and message.tool_calls:
                    for tool_call in message.tool_calls:
                        print(f"Searching: {tool_call["args"].get('query','')}")

                elif isinstance(message,ToolMessage):
                    print(f"fetched results for: {message.name}")


                elif isinstance(message,AIMessage):
                    print(f"\nReports:\n{message.content}")
                    final_report = message.content
                    filename = input("Enter filename you want to save the report into pdf")     


def create_pdf(report_text,filename):
        
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True,margin=15)
    lines = report_text.splitlines()

    for line in lines:
        if line.startswith("##"):
            text = line.replace("##","")
            pdf.set_font("Arial",style="B",size=16)
            pdf.cell(0,10,txt=text,ln=True)

        elif line.startswith("###",""):
            text = line.replace("###","")
            pdf.set_font("Arial",style="B",size=13)
            pdf.cell(0,8,txt=text,ln=True)   

        elif line.startswith("- "):
            text = "• " + line[2:]
            pdf.set_font("Arial",size=11)
            pdf.cell(0,7,txt=text,ln=True)


        elif line.strip() == "":
            pdf.ln(4) 

        else:
            pdf.set_font("Arial",size=13)
            pdf.multi_cell(0,7,txt=line)


    pdf.output(filename)
    print(f"PDF: {filename} created succesfully")


if final_report:
    create_pdf(final_report,filename)                  
