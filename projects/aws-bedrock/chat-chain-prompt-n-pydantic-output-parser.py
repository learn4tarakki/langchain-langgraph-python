from langchain_aws import ChatBedrockConverse
from langchain.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel

class Person(BaseModel):
    name: str

class People(BaseModel):
    people: list[Person]

parser = PydanticOutputParser(pydantic_object=People)

# Fixed system template with proper escaping of JSON structure
system_template = """You are a helpful assistant that always responds in JSON format.
Extract names from the input and return them in the following JSON structure:
{{
    "people": [
        {{"name": "extracted_name"}}
    ]
}}

Only include the name, no other information. Always return valid JSON that matches this exact structure.
{format_instructions}
"""

prompt = ChatPromptTemplate.from_messages([
    ("system", system_template),
    ("human", "{query}")
])

prompt_with_instructions = prompt.partial(format_instructions=parser.get_format_instructions())

query = "Anna is 23 years old and she is 6 feet tall"

llm = ChatBedrockConverse(
    model="amazon.nova-lite-v1:0"
)

try:
    chain = prompt_with_instructions | llm | parser
    response = chain.invoke({"query": query})
    print(response)
except Exception as e:
    print(f"Error: {str(e)}")
    raw_response = prompt_with_instructions | llm
    print("\nRaw LLM response:")
    print(raw_response.invoke({"query": query}))

## output 
## people=[Person(name='Anna')]    