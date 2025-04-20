import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI

async def main():
    # Initialize the model
    model = ChatOpenAI(model="gpt-4o")
    
    async with MultiServerMCPClient(
        {
            "math": {
                "command": "python",
                # Make sure to update to the full absolute path to your math_server.py file
                "args": ["/home/ubu/Documents/work/l4t/ai-python-series/langchain-langgraph-python/projects/langgraph/scripts/mcp/mcp-tool-server1.py"],
                "transport": "stdio",
            },
            "weather": {
                # make sure you start your weather server on port 8000
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            }
        }
    ) as client:
        # Create the agent with the tools from the MCP client
        agent = create_react_agent(model, client.get_tools())
        
        # Process math query
        print("Asking math question...")
        math_response = await agent.ainvoke({"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]})
        print("Math response:", math_response)
        
        # Process weather query
        print("Asking weather question...")
        weather_response = await agent.ainvoke({"messages": [{"role": "user", "content": "what is the weather in nyc?"}]})
        print("Weather response:", weather_response)

# Run the async function
if __name__ == "__main__":
    asyncio.run(main())

