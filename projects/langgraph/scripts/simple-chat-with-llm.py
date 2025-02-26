from typing import Annotated
from typing_extensions import TypedDict
from IPython.display import Image, display

from langchain_aws import ChatBedrockConverse
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]


graph = StateGraph(State)

llm = ChatBedrockConverse(model="amazon.nova-lite-v1:0")

def chatbot(state: State):
    ai_message = llm.invoke(state["messages"])
    return {"messages": [ai_message]}

# Node
graph.add_node("chatbot", chatbot)

# Edges
graph.add_edge(START, "chatbot")
graph.add_edge("chatbot", END)

# Compile
compiled_graph = graph.compile()

result = compiled_graph.invoke({"messages": [{"role": "user", "content": "Hey! can you suggest me a one book on AI?"}]})

print("Assistant:", result["messages"][-1].content)

try:
    display(Image(compiled_graph.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass
