from langchain_ollama import ChatOllama

model = ChatOllama(model="deepseek-r1:1.5b", base_url="http://localhost:11434")

messages = [("system","you are a scientist, respond in 10 words"), ("human", "how can i make rocket.")]

response = model.invoke(messages)

print(response.content)

