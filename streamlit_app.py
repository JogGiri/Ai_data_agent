import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from agent_tools import get_schema, execute_query
from langchain.agents import create_agent
import json

load_dotenv()

st.set_page_config(page_title="Database AI Agent", layout="wide")
st.title("🤖 Database AI Agent")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    model_name = st.selectbox(
        "Select Model",
        ["gpt-4o-mini", "gpt-4-turbo", "gpt-4"],
        index=0
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.7)

    st.divider()
    st.header("🔧 Display Options")
    show_tool_calls = st.toggle("Show Tool Calls", value=True)

    st.divider()
    st.info("💡 Ask questions about your PostgreSQL database. The agent will use available tools to fetch schema and execute queries.")

# Initialize session state for conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    model = ChatOpenAI(
        model=model_name,
        temperature=temperature
    )
    tools = [get_schema, execute_query]
    st.session_state.agent = create_agent(
        model=model,
        tools=tools,
        system_prompt="""
You are a helpful database assistant who can answer questions about the PostgreSQL database.
Use the available tools to:
1. First use get_schema to understand the database structure when asked about tables or schema
2. Use execute_query to run SQL queries and fetch data
3. Provide clear explanations of the results

Always be helpful and provide accurate information based on the database."""
    )

# Main chat area
col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("💬 Chat History")

    # Create a container for chat messages
    chat_container = st.container(border=True)

    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                if "tool_calls" in message and show_tool_calls:
                    with st.expander("🔨 Tool Calls"):
                        for tool_call in message["tool_calls"]:
                            st.code(json.dumps(tool_call, indent=2), language="json")
                if "tool_results" in message and show_tool_calls:
                    with st.expander("📊 Tool Results"):
                        st.text(message["tool_results"][:500] + ("..." if len(message["tool_results"]) > 500 else ""))

with col2:
    st.subheader("📋 Session Info")
    st.metric("Messages", len(st.session_state.messages))
    st.metric("Model", model_name)
    st.metric("Temp", temperature)

# Chat input
st.divider()
user_input = st.chat_input("Ask a question about your database...")

if user_input:
    # Add user message to history
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with chat_container:
        with st.chat_message("user"):
            st.write(user_input)

    # Get agent response
    with chat_container:
        with st.chat_message("assistant"):
            with st.spinner("🤔 Thinking..."):
                try:
                    response = st.session_state.agent.invoke({
                        "messages": [{"role": "user", "content": user_input}]
                    })

                    # Extract response content and tool information
                    agent_message = response["messages"][-1]
                    agent_response = agent_message.content

                    # Store message with tool info if available
                    message_data = {
                        "role": "assistant",
                        "content": agent_response
                    }

                    # Try to extract tool calls from response
                    if hasattr(agent_message, 'tool_calls') and agent_message.tool_calls:
                        message_data["tool_calls"] = [
                            {
                                "tool": call.name,
                                "args": call.args
                            }
                            for call in agent_message.tool_calls
                        ]

                    # Look for tool results in the response messages
                    for msg in response["messages"]:
                        if msg.type == "tool":
                            if "tool_results" not in message_data:
                                message_data["tool_results"] = msg.content

                    st.session_state.messages.append(message_data)

                    st.write(agent_response)

                    # Show tool calls if available and toggle is on
                    if "tool_calls" in message_data and show_tool_calls:
                        with st.expander("🔨 Tool Calls"):
                            for tool_call in message_data["tool_calls"]:
                                st.code(json.dumps(tool_call, indent=2), language="json")

                    if "tool_results" in message_data and show_tool_calls:
                        with st.expander("📊 Tool Results"):
                            st.text(message_data["tool_results"][:500] + ("..." if len(message_data["tool_results"]) > 500 else ""))

                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": f"Error: {str(e)}"
                    })

# Footer
st.divider()
st.caption("🚀 Database AI Agent - Powered by LangChain & Streamlit")
