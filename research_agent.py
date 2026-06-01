from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage , AIMessage , ToolMessage
from fpdf import FPDF
import markdown2
from weasyprint import HTML
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


agent  =create_agent(
    model = llm,
    tools=[search_tool]
)

def create_pdf(report_text,filename):
    html_content = markdown2.markdown(report_text)
    HTML(string=html_content).write_pdf(filename)
    print(f"PDF: {filename} created succesfully")
# def create_pdf(report_text,filename):
        
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Helvetica",size=12)
#     pdf.set_auto_page_break(auto=True,margin=15)
#     lines = report_text.splitlines()

#     for line in lines:
#         line = line.strip()
#         line = line.replace("**","")
#         line = line.replace("__","")
#         line = line.replace("`","")
#         def safe_text(text):
#             return (text.encode("latin-1","replace").decode("latin-1"))
#         if line.startswith("###"):
#             text = line.replace("###","").strip()
#             pdf.set_font("Helvetica",style="B",size=13)
#             pdf.multi_cell(0,8,text=safe_text(text))  


#         elif line.startswith("##"):
#             text = line.replace("##","").strip()
#             pdf.set_font("Helvetica",style="B",size=16)
#             pdf.multi_cell(0,10,text=safe_text(text))

         

#         elif line.startswith("- "):
#             text = "- " + line[2:]
#             pdf.set_font("Helvetica",size=11)
#             pdf.multi_cell(0,7,text=safe_text(text))




#         elif line == "":
#             pdf.ln(4) 

#         else:
#             pdf.set_font("Helvetica",size=13)
#             stripped = line.strip()
#             if stripped and set(stripped) <= {"-","="}:
#                 continue
#             if line.startswith("|"):
#                 continue
            
#             safe_line = line.encode("latin-1","replace").decode("latin-1")
#             if not safe_line:
#                 continue
#             if len(safe_line) > 500:
#                 safe_line = safe_line[:500] + "....."
#             print("PDF-line: ",repr(safe_line))
#             pdf.multi_cell(w=0,h=7,text=safe_text(safe_line))


#     pdf.output(filename)
#     print(f"PDF: {filename} created succesfully")

while True:

    

    topic = input("Enter research topic(or quit:'quit'): ")

    final_report = None

    if topic.lower() == "quit":
        print("Trau says goodbye!!..")
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
                        query = tool_call.get("args",{}).get("query","")
                        print(f"Searching: {query}")

                elif isinstance(message,ToolMessage):
                    print(f"fetched results for: {message.name}")


                elif isinstance(message,AIMessage):
                    print(f"\nReports:\n{message.content}")
                    final_report = message.content
                         

    if final_report:
        filename = input("Enter filename you want to save the report into pdf: ")
        if not filename.endswith(".pdf"):
            filename += ".pdf"
        create_pdf(final_report,filename)     




                 
