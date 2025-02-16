## Youtube Channel
- Watch videos on [Learn4Tarakki Channel](https://www.youtube.com/channel/UCO251AKqx8iSssbN66eECLA)

## Support Jupyter within VSCode
- Adding support for .
  - uv add --dev ipykernel
  - uv add --dev uv
  - In notebook, you can install packages into .venv without having change in pyproject.toml 
    - !uv pip install langgraph   
    - to run, same in hosted google colab, remove prefix `!uv` from installation commands
    - if you still want to impact both .venv and pyproject.toml file, then
      - !uv add langgraph

### How Agent works in LangGraph
  - LangGraph implemented ReAct Agent Reference Paper with some modifications in prebuilt - create_react_agent
   - Core Concepts
    - Planning
    - Tool Calling
    - Memory
   - User -> Query -> LLM Client (binds with Tools) -> LLM 
   - LLM Client keeps calling LLM in while loop utilising tool when necessary 
   - LLM Client stops when satisfactory result is found and respond back to user

### Agents 
 - Langchain legacy use - AgentExecutor 
  ```python 
  agent = create_tool_calling_agent(model, tools, prompt)
  agent_executor = AgentExecutor(agent=agent, tools=tools)  
  agent_executor.invoke({"input": query})
  ```
 - LangGraph use - create_react_agent prebuilt helper method 
  ```python
  langgraph_agent_executor = create_react_agent(model, tools)
  messages = langgraph_agent_executor.invoke({"messages": [("human", query)]})
  {
    "input": query,
    "output": messages["messages"][-1].content,
  }
  ```

## Prompt use 
```
const promptTemplate = ChatPromptTemplate.fromMessages([
  ["system","You are an expert"],
  ["human", "{query}"],
]);

```
## Types of roles 
- system
- user (or human)
- assistant (ai response)
- tool 

## Types of content 
- SystemMessage: corresponds to system role - not all models support it. so, better stick with HumanMessage 
- HumanMessage: corresponds to user role
- AIMessage: corresponds to assistant role (response from llm)
- AIMessageChunk: corresponds to assistant role, used for streaming responses
- ToolMessage: corresponds to tool role
- RemoveMessage - only by LangGraph to manage chat history

## Common Approach
```
from langchain_core.messages import HumanMessage

model.invoke([HumanMessage(content="Hello, how are you?")])
```