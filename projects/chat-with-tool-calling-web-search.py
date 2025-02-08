import os
from dotenv import load_dotenv
from langchain_core.messages import  HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from duckduckgo_search import DDGS
from devtools import debug

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

@tool
def search(query: str, num_results: int = 3):
    """Search DuckDuckGo for the given query and return the top results."""
    results = DDGS().text(query, max_results=num_results)
    return results

llm_with_tools = llm.bind_tools([search])

messages = [SystemMessage("Answer the following question. If you don't know the answer, say 'I don't know, but here are some search results:' and provide search results."), 
            HumanMessage("What is the latest news on AI?")]

response = llm_with_tools.invoke(messages) 

messages.append(response)

debug(response.tool_calls)

for tool_call in response.tool_calls:
    selected_tool = {"search": search}[tool_call["name"].lower()]
    tool_msg = selected_tool.invoke(tool_call)
    messages.append(tool_msg)

# debug(messages)    

res = llm_with_tools.invoke(messages)

print(res.content) # final output 

"""
Output:
projects/chat-with-tool-calling-web-search.py:29 <module>
    response.tool_calls: [
        {
            'name': 'search',
            'args': {
                'query': 'latest news on AI',
                'num_results': 3,
            },
            'id': 'call_tPsKK0oPSzg9kvOjVUEVBd8r',
            'type': 'tool_call',
        },
    ] (list) len=1
I don't know, but here are some search results:

1. [The Latest AI News and Analysis - PCMag](https://www.pcmag.com/news/categories/ai): The AI agent runs on a version of OpenAI's upcoming o3 model, but for now, you need a $200-per-month Pro subscription to try it out. (4 days ago)

2. [Artificial Intelligence News | MIT News](https://news.mit.edu/topic/artificial-intelligence2): Details on a technique using generative AI to emulate the dynamics of molecules, which could help scientists make more accurate forecasts.

3. [AI News & Artificial Intelligence | TechCrunch](https://techcrunch.com/category/artificial-intelligence/): Covers the latest on artificial intelligence and machine learning technology, the companies building them, and the ethical issues surrounding AI.
"""