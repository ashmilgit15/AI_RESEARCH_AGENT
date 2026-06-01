from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage , AIMessage , ToolMessage

import os

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