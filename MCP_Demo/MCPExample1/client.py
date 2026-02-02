import asyncio
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("CEREB")

client_ai = Cerebras(api_key=api_key)

async def run_chat_loop():
    server_params = StdioServerParameters(
        command=['python3']
        args=['MCP_Demo/MCPExample1/server.py'  ]
    )

    async with stdio_client(server_params) as (read,write):
        async with ClientSession(read, write) as session:
            
            mcp_tools = await session.list_tools()

            cerebras_tools = []
            for tools in mcp_tools:
                cerebras_tools.append({
                    "type":"function",
                    "function":{
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.inputSchema
                    }
                })

            print(f"Loaded {len(cerebras_tools)} tools from MCP server.")

            messages = []

            while True:
                user_input = input("\nYou: ")

                if user_input.lower() in ['exit','quit']:
                    print("Exiting chat.")
                    break

                messages.append({'role':"user","content":user_input})

                response = client_ai.chat.completions.create(
                    model='llama3.1-8b',
                    messages=messages,
                    tools=cerebras_tools
                )

                ai_msg = response.choices[0].message

                if ai_msg.tool_calls:
                    print(f"AI wants to use tools ...")
                    messages.ppend(ai_msg)