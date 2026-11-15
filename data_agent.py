from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from agent_tools import get_schema,execute_query
from langchain.messages import HumanMessage, SystemMessage, AIMessage
from langchain.agents import create_agent

load_dotenv()

# model = ChatGoogleGenerativeAI(
#     model="gemini-3.8-flash",
# )
model = ChatOpenAI(
    model="gpt-6-luna")

tools=[get_schema,execute_query]

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="""
You are a helpful assistant who can answer questions about the postgres database. 
Use the tools below to answer the questions.
"""
)

while True:
    user_input = input("User: ")
    if user_input == "exit":
        break
    response = agent.invoke({"messages":[{"role":"user","content":user_input}]})
    print("Agent: ",response["messages"][-1].text)