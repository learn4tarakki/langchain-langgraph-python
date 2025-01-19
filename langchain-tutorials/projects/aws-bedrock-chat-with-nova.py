from langchain_aws import ChatBedrockConverse

llm = ChatBedrockConverse(model="amazon.nova-lite-v1:0")

messages = [("system", "you are a general physician."), ("user", "what you suggest for mild fever in 10 words.")]

ai_message = llm.invoke(messages)

print(ai_message.content)


