import asyncio

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams
from agents.items import ToolCallOutputItem
from devtools import pprint

from dotenv import load_dotenv
load_dotenv()

mcp_server = MCPServerStreamableHttp(
    params=MCPServerStreamableHttpParams(
        url="http://localhost:8000/mcp",
    )
)

agent = Agent(
    name="Agent",
    mcp_servers=[mcp_server]
)


async def main() -> str:

    await mcp_server.connect()
    result = await Runner.run(agent, "Please call the show_external_url tool")
    await mcp_server.cleanup()

    for item in result.new_items:
        if isinstance(item, ToolCallOutputItem):
            return item.raw_item

if __name__ == "__main__":
    result = asyncio.run(main())
    pprint(result)