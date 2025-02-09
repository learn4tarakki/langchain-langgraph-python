from langchain_aws import ChatBedrockConverse
from devtools import debug 

model = ChatBedrockConverse(model="amazon.nova-lite-v1:0")

messages = [("system", "you are a general physician. suggest everything in 10 words."), 
            ("human", "what you suggest for mild fever.")
           ]

response = model.invoke(messages)

debug(response) # we need to extract explicitly 