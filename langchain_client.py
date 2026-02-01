import asyncio
from plistlib import load
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
llm = ChatOpenAI()

async def main():
    client = MultiServerMCPClient(
        {
            "math": {
                "transport": "stdio",
                "command": "uv",
                "args": [
                    "run",
                    r"c:\Users\hamma\cursorProjects\langchain-course-mcp-servers\servers\math_server.py"
                ],
            },
            "weather": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            },
        }
    )
    tools = await client.get_tools()
    agent = create_agent(llm, tools)
    result = await agent.ainvoke({"messages": "What is 2 + 2?"})
    # result = await agent.ainvoke(
    #     {"messages": "What is the weather in San Francisco?"}
    # )

    print(result["messages"][-1].content)

if __name__ == "__main__":
    asyncio.run(main())