import asyncio
from dotenv import load_dotenv
import os
from mcp import ClientSession, StdioServerParameters
from langchain_openai import ChatOpenAI
from mcp.client.stdio import stdio_client
from langchain.agents import create_agent
from langchain_mcp_adapters.tools import load_mcp_tools
from langchain_core.messages import HumanMessage

load_dotenv()
llm = ChatOpenAI()

stdio_server_params = StdioServerParameters(
    command="uv",  # or "uv.exe"
    args=[
        "run",
        r"c:\Users\hamma\cursorProjects\langchain-course-mcp-servers\servers\math_server.py",
    ],
)

async def main():
    async with stdio_client(stdio_server_params) as (read, write):
        async with ClientSession(read_stream=read, write_stream=write) as session:
            await session.initialize()
            print("session initialized")
            tools = await load_mcp_tools(session)

            agent = create_agent(llm, tools)

            result = await agent.ainvoke(
                {"messages": [HumanMessage(content="What is 54 + 2 * 3?")]}
            )
            print(result["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
