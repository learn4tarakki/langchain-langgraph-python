from langchain_deepseek import ChatDeepSeek
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatDeepSeek(model="deepseek-chat", api_key=os.getenv("DEEPSEEK_API_KEY"))

messages = [("system", "you are a general physician."), ("user", "what you suggest for mild fever in 10 words.")]

response = model.invoke(messages)

print(response.content)

