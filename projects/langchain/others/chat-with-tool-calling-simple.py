import os
from dotenv import load_dotenv
from langchain_core.messages import  HumanMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field, ValidationError
from devtools import debug

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

class AddInput(BaseModel):
    a: int = Field(description="first number", multiple_of=2)
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

messages = [HumanMessage("sum of 2, 2 is and multiplication of 4, 3 is")]

response = llm_with_tools.invoke(messages) 

messages.append(response)

# debug(response.tool_calls)

try:
    for tool_call in response.tool_calls:
        selected_tool = {"add": add, "multiply": multiply}[tool_call["name"].lower()]
        tool_msg = selected_tool.invoke(tool_call)
        messages.append(tool_msg)

    # debug(messages)    

    res = llm_with_tools.invoke(messages)

    debug(res.content) # final output 

except ValidationError as e: 
    debug(e.errors())

"""
Output - In case of Validation Error, when first number in query is 1 and all debug are printed
    response.tool_calls: [
        {
            'name': 'add',
            'args': {
                'a': 1,
                'b': 2,
            },
            'id': 'call_bpqXMtaMNV13SKTnA1OVSxa9',
            'type': 'tool_call',
        },
        {
            'name': 'multiply',
            'args': {
                'a': 4,
                'b': 3,
            },
            'id': 'call_vgXpMmzGt7cvXnbpkVv7cxbE',
            'type': 'tool_call',
        },
    ] (list) len=2

e.errors(): [
        {
            'type': 'multiple_of',
            'loc': ('a',),
            'msg': 'Input should be a multiple of 2',
            'input': 1,
            'ctx': {
                'multiple_of': 2,
            },
            'url': 'https://errors.pydantic.dev/2.10/v/multiple_of',
        },
    ] (list) len=1
"""    

"""
Output - When first number in query is 2 - means multiple of 2, which does not cause validation error and all debug are printed
projects/chat-with-tool-calling.py:41 <module>
    response.tool_calls: [
        {
            'name': 'add',
            'args': {
                'a': 2,
                'b': 2,
            },
            'id': 'call_VFBUNjcUOAkifFQ2sdiG6wag',
            'type': 'tool_call',
        },
        {
            'name': 'multiply',
            'args': {
                'a': 4,
                'b': 3,
            },
            'id': 'call_SPFRCbIWgjWaZ1tj3wGidBAu',
            'type': 'tool_call',
        },
    ] (list) len=2
projects/chat-with-tool-calling.py:49 <module>
    messages: [
        HumanMessage(
            content='sum of 2, 2 is and multiplication of 4, 3 is',
            additional_kwargs={},
            response_metadata={},
        ),
        AIMessage(
            content='',
            additional_kwargs={
                'tool_calls': [
                    {
                        'id': 'call_VFBUNjcUOAkifFQ2sdiG6wag',
                        'function': {
                            'arguments': '{"a": 2, "b": 2}',
                            'name': 'add',
                        },
                        'type': 'function',
                    },
                    {
                        'id': 'call_SPFRCbIWgjWaZ1tj3wGidBAu',
                        'function': {
                            'arguments': '{"a": 4, "b": 3}',
                            'name': 'multiply',
                        },
                        'type': 'function',
                    },
                ],
                'refusal': None,
            },
            response_metadata={
                'token_usage': {
                    'completion_tokens': 51,
                    'prompt_tokens': 106,
                    'total_tokens': 157,
                    'completion_tokens_details': {
                        'accepted_prediction_tokens': 0,
                        'audio_tokens': 0,
                        'reasoning_tokens': 0,
                        'rejected_prediction_tokens': 0,
                    },
                    'prompt_tokens_details': {
                        'audio_tokens': 0,
                        'cached_tokens': 0,
                    },
                },
                'model_name': 'gpt-4o-2024-08-06',
                'system_fingerprint': 'fp_50cad350e4',
                'finish_reason': 'tool_calls',
                'logprobs': None,
            },
            id='run-886905f8-ed7f-4ba3-9bb3-f46858bc0777-0',
            tool_calls=[
                {
                    'name': 'add',
                    'args': {
                        'a': 2,
                        'b': 2,
                    },
                    'id': 'call_VFBUNjcUOAkifFQ2sdiG6wag',
                    'type': 'tool_call',
                },
                {
                    'name': 'multiply',
                    'args': {
                        'a': 4,
                        'b': 3,
                    },
                    'id': 'call_SPFRCbIWgjWaZ1tj3wGidBAu',
                    'type': 'tool_call',
                },
            ],
            usage_metadata={
                'input_tokens': 106,
                'output_tokens': 51,
                'total_tokens': 157,
                'input_token_details': {
                    'audio': 0,
                    'cache_read': 0,
                },
                'output_token_details': {
                    'audio': 0,
                    'reasoning': 0,
                },
            },
        ),
        ToolMessage(
            content='4',
            name='add',
            tool_call_id='call_VFBUNjcUOAkifFQ2sdiG6wag',
        ),
        ToolMessage(
            content='12',
            name='multiply',
            tool_call_id='call_SPFRCbIWgjWaZ1tj3wGidBAu',
        ),
    ] (list) len=4
projects/chat-with-tool-calling.py:53 <module>
    res.content: 'The sum of 2 and 2 is 4, and the multiplication of 4 and 3 is 12.' (str) len=65
"""    