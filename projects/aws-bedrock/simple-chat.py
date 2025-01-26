from langchain_aws import ChatBedrockConverse

model = ChatBedrockConverse(model="amazon.nova-lite-v1:0")

messages = [("system", "you are a general physician."), 
            ("human", "what you suggest for mild fever in 10 words.")
           ]

response = model.invoke(messages)

print(response.content) # we need to extract explicitly 