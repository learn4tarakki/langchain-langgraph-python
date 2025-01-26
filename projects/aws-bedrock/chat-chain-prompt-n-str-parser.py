from langchain_aws import ChatBedrockConverse
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

model = ChatBedrockConverse(model="amazon.nova-lite-v1:0")

prompt =  ChatPromptTemplate.from_messages(
         [("system", "you are a general physician."), 
          ("human", "{input}")           
         ])

chain = prompt | model | StrOutputParser()

response = chain.invoke({"input": "what you suggest for mild fever in 10 words."})

print(response)