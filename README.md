## Prompt use 
```
const promptTemplate = ChatPromptTemplate.fromMessages([
  ["system","You are an expert"],
  ["human", "{query}"],
]);

```

## Types of roles 
- system
- user 
- assistant 
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