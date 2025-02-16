from typing_extensions import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display

def reducer(a: list, b: int | None) -> list:
    if b is not None: 
       return a + [b]
    return a     

class State(TypedDict):
    messages: Annotated[list, reducer]


graph = StateGraph(State)

def add(num1: int, num2: int) -> int: 
    return num1 + num2 


def print(a: str) -> None: 
    print(a) 


graph.add_node('addition', add)
graph.add_node('printing', print)

graph.add_edge(START, 'addition')
graph.add_edge('addition', 'printing')
graph.add_edge('printing', END)

compiled = graph.compile()

try:
    display(Image(compiled.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass

