from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import execute_query
from langchain.messages import HumanMessage, SystemMessage, AIMessage

load_dotenv()

# model = ChatGoogleGenerativeAI(
#     model="gemini-3.8-flash",
# )
model = ChatOpenAI(
    model="gpt-6-luna",
)

conversation = []

while True:
    inputs = input('Your Question: ')

    if inputs == "exit":
        break
    prompt=f"""
    Give me postgres compatible sql for given quetion for given schema. Give me only query.
    quation : {inputs}
    table_name : returns
    """

    response = model.invoke(prompt)
    print("Query :",response.text)
    result = execute_query(response.text)
    print("Result",result)
    # conversation.append(HumanMessage(content=prompt))
    # response = model.invoke(conversation)
    # print(response.text)
   
    # conversation.append(AIMessage(content=response.text))

    
# print(conversation)
# def main():
#     print("Hello from ai-agent-demo!")


# if __name__ == "__main__":
#     main()
