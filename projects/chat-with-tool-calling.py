import os
from dotenv import load_dotenv
from langchain_core.messages import  HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from devtools import debug

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

class AddInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")

class MultiplyInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")


@tool("add", args_schema=AddInput, return_direct=True)
def add(a: int, b: int) -> int:
    """Adds a and b."""
    return a + b

@tool("multiply", args_schema=MultiplyInput, return_direct=True)
def multiply(a: int, b: int) -> int:
    """Multiply a and b."""
    return a * b


llm_with_tools = llm.bind_tools([add, multiply])

messages = [HumanMessage("sum of 1, 2 is and multiplication of 4, 3 is")]

response = llm_with_tools.invoke(messages) 

messages.append(response)

debug(response.tool_calls)

for tool_call in response.tool_calls:
    selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)

debug(messages)    

res = llm_with_tools.invoke(messages)

debug(res.content) # final output 
