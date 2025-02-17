from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display


class State(TypedDict):
    number1: int
    number2: int
    result: int


graph = StateGraph(State)


def add(state: State) -> State:
    result = state["number1"] + state["number2"]
    return {"result": result}


def show(state: State) -> None:
    print(f"Addition of {state['number1']} & {state['number2']} is {state['result']}")


graph.add_node("add", add)
graph.add_node("show", show)

graph.add_edge(START, "add")
graph.add_edge("add", "show")
graph.add_edge("show", END)

compiled = graph.compile()

compiled.invoke({"number1": 1, "number2": 2})

try:
    display(Image(compiled.get_graph().draw_mermaid_png()))
except Exception:
    # This requires some extra dependencies and is optional
    pass
