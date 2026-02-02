import asyncio

import os

from mcp import ClientSession, StdioServerParameters 
from mcp.client.stdio import stdio_client

from google import genai
from google.genai import types

async def run_client():
    #The following code tells the client how to launch the server script:
    server_params = StdioServerParameters(
        command='python3',
        args=['MCP_Demo/MCP_DEMO_Ex_1/main.py']
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read,write) as session:
            #The Client asks : "What tools do i have? "
            print('---Discovery---')
            tools = await session.list.tools()
            print(f"Connected to server. Found Tools : {tools.tools[0].name}")
            print(f"Tools Description: {tools.tools[0].description}")

            #Normally an LLM would decide which tool to use based on user input.
