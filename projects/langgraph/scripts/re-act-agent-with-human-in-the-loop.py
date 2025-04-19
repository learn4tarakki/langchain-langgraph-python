from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
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

graph = create_react_agent(model, tools=tools, interrupt_before=["tools"], checkpointer=memory)

inputs = {"messages": [("user", "what is the weather in SF, CA")]}

def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()

print_stream(graph.stream(inputs, config=config, stream_mode="values"))

# to check the next state, where it halts 
snapshot = graph.get_state(config)
print("Next step: ", snapshot.next)

# to continue with affirmation 
# print_stream(graph.stream(None, config, stream_mode="values"))

# to adjust state as per human input and then continue
state = graph.get_state(config)

last_message = state.values["messages"][-1]
last_message.tool_calls[0]["args"] = {"location": "San Francisco"} # instead of directly manipulating, we can use input() to aks input from user 

graph.update_state(config, {"messages": [last_message]})
print_stream(graph.stream(None, config, stream_mode="values"))