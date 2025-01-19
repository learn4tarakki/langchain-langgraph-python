from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

messages = [("system", "you are a general physician."), ("user", "what you suggest for mild fever in 10 words.")]

ai_message = llm.invoke(messages)

print(ai_message.content)

