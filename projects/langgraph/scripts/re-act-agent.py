from typing import Literal
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from IPython.display import Image, display
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

@tool
def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")


tools = [get_weather]

graph = create_react_agent(model, tools=tools)  # Initial State is { messages: [] }

inputs = {"messages": [("user", "what is the weather in sf")]}

# Invoke approach, here last message is AIMessage
res = graph.invoke(inputs)
print(res["messages"][-1].content)

# State at every interaction: 
    # messages: [HumanMessage], 
    # messages: [HumanMessage, AIMessage], 
    # messages: [HumanMessage, AIMessage, ToolMessage], 
    # messages: [HumanMessage, AIMessage, ToolMessage, AIMessage]
# def print_stream(stream):
#     for s in stream:
#         message = s["messages"][-1]
#         if isinstance(message, tuple):
#             print(message)
#         else:
#             message.pretty_print()

# print_stream(graph.stream(inputs, stream_mode="values"))

# to demo, that it does not retain last conversation, without using memory and thread config
# inputs = {"messages": [("user", "What's it known for?")]}
# print_stream(graph.stream(inputs, stream_mode="values"))

try:
    display(Image(graph.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass