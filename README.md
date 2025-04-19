### Youtube Channel
- Watch videos on [Learn4Tarakki Channel](https://www.youtube.com/channel/UCO251AKqx8iSssbN66eECLA)

### Support Jupyter within VSCode 
- Adding support for .
  - uv add --dev ipykernel
  - uv add --dev uv
  - In notebook, you can install packages into .venv without having change in pyproject.toml 
    - !uv pip install langgraph   
    - to run, same in hosted google colab, remove prefix `!uv` from installation commands
    - if you still want to impact both .venv and pyproject.toml file, then
      - !uv add langgraph
  - Imp. - to avoid jupyter cache, use Restart option in top menu    

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
### Prompt use 
```
const promptTemplate = ChatPromptTemplate.fromMessages([
  ["system","You are an expert"],
  ["human", "{query}"],
]);

```
### Types of roles 
- system
- user (or human)
- assistant (ai response)
- tool 

### Types of content 
- SystemMessage: corresponds to system role - not all models support it. so, better stick with HumanMessage 
- HumanMessage: corresponds to user role
- AIMessage: corresponds to assistant role (response from llm)
- AIMessageChunk: corresponds to assistant role, used for streaming responses
- ToolMessage: corresponds to tool role
- RemoveMessage - only by LangGraph to manage chat history

### Common Approach
```
from langchain_core.messages import HumanMessage

model.invoke([HumanMessage(content="Hello, how are you?")])
```   

### Streaming 
- Stream mode - values, here Chunks are [State1, State2, State3], State1 is complete new state after Node1, similarly for State2 
  - In case of Pre-built Agent, Graph State is {messages:[]}, hence new states keep having additional message and 
    - Chunks are: 
      - State1 -> {messages:[HumanMessage(content='what is the weather in sf', additional_kwargs={}, response_metadata={}, id='<UUID>')]}
      - State2 -> {messages:[HumanMessage(content='what is the weather in sf', <other args>), AIMessage(content='<RESPONSE CONTENT>', <other args>)]}
```
for chunk in graph.stream({"topic": "ice cream"},stream_mode="values",):
    print(chunk)
```
- Stream mode - updates, here Chunks are [State updation by Node 1, State updation by Node 2], State updation means only portion of state, updated by Node  
```
for chunk in graph.stream({"topic": "ice cream"},stream_mode="updates",):
    print(chunk)
```
- Stream mode - messages, here Chunks are only of AIMessage, but token by token and [AIMessage1 Chunk1, AIMessage1 Chunk2, AIMessage2 Chunk1], here AIMessage get chunked into multiple, so the content will come in parts. Each of chunk comes with metadata as well. 
  - Example - AIMessage(content='It's always sunny in sf') will comes as: 
      -  AIMessage(content='It's')
      -  AIMessage(content='always')
      - and so on..  
```
for message_chunk, metadata in graph.stream({"topic": "ice cream"},stream_mode="messages",):
    if message_chunk.content:
        print(message_chunk.content, end="|", flush=True)
```

### Human in the loop 
- Approach
  - interrupt & collect input using interrupt() and then resume using Command(resume=<User Input>) 
- Scenarios
  - Re-Act Agent (Prebuilt) - interrupt every tool call 
    - use interrupt_before / interrupt_after params of create_react_agent to interrupt before and after tool call. 
    - here, interrupt is not tool specific, it interrupt before or after every tool call
    - then collect, manipulate & resume:
       - collect user input using input()
       - manipulate last message in state and 
       - resume using:  
          - graph.update_state(config, {"messages": [last_message]})
          - print_stream(graph.stream(None, config, stream_mode="values"))  
  - Re-Act Agent (Prebuilt) - interrupt on specific tool (do not use interrupt_before or interrupt_after) / Custom Agent  
    - create custom graph   
      - 1st node for re-act agent or custom Agent - Agent Node 
      - 2nd node act as toolnode for re-act or custom agent which won't be interrupted - ToolNode (holds tools)
      - 3rd node for having code to interrupt & collect user input using interrupt() - AskHuman Node 
      - add conditional edge to invoke AskHuman Node so that we can interrupt and ask for user input 
      - then invoke graph 
      - finally, resume graph using Command(resume=<User Input>), here User Input is one that we collected from user when interruption happened