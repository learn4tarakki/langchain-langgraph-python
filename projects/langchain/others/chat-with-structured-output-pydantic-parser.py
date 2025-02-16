from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import Optional
from devtools import debug
import os

# Pydantic
class Joke(BaseModel):
    setup: str = Field(description="The setup of the joke")
    punchline: str = Field(description="The punchline to the joke")
    rating: Optional[int] = Field(
        default=None, description="How funny the joke is, from 1 to 10"
    )

model = ChatOpenAI(model="gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))


structured_model = model.with_structured_output(Joke)

response = structured_model.invoke("Tell me a joke about cats")

debug(response)