from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))

messages = [("system", "you are a general physician."), ("user", "what you suggest for mild fever in 10 words.")]

response = model.invoke(messages)

print(response.content)

