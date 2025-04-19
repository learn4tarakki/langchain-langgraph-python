from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from IPython.display import Image, display
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

@tool
def get_weather(location: str):
    """Use this to get weather information from a given location."""
    if location.lower() in ["nyc", "new york"]:
        return "It might be cloudy in nyc"
    elif location.lower() in ["sf", "san francisco"]:
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown Location")

tools = [get_weather]

memory = MemorySaver()

config = {"configurable": {"thread_id": "1"}}

graph = create_react_agent(model, tools=tools, checkpointer=memory)

inputs = {"messages": [("user", "what is the weather in sf")]}

# State at every interaction: 
    # Interaction 1
        # messages: [HumanMessage], 
        # messages: [HumanMessage, AIMessage], 
        # messages: [HumanMessage, AIMessage, ToolMessage], 
        # messages: [HumanMessage, AIMessage, ToolMessage, AIMessage]
    # Interaction 2
        # messages: [HumanMessage, AIMessage, ToolMessage, AIMessage, HumanMessage]
        # messages: [HumanMessage, AIMessage, ToolMessage, AIMessage, HumanMessage, AIMessage]
def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

print_stream(graph.stream(inputs, config=config, stream_mode="values"))

inputs = {"messages": [("user", "What's it known for?")]}

print_stream(graph.stream(inputs, config=config, stream_mode="values"))

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass