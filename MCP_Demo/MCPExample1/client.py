import asyncio
import os
import sys
from contextlib import AsyncExitStack
from pathlib import Path

import google.generativeai as genai
from dotenv import load_dotenv

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

GEMINI_MODEL = "models/gemini-3-flash-preview"


class MCPClient:
    def __init__(self):
        self.session: ClientSession | None = None
        self.exit_stack = AsyncExitStack()
        self._model = None

    @property
    def model(self):
        if self._model is None:
            genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
            self._model = genai.GenerativeModel(GEMINI_MODEL)
        return self._model

    async def connect_to_server(self, server_script_path: str):
        is_python = server_script_path.endswith(".py")
        is_js = server_script_path.endswith(".js")

        if not (is_python or is_js):
            raise ValueError("Server script must be .py or .js")

        if is_python:
            path = Path(server_script_path).resolve()
            server_params = StdioServerParameters(
                command="uv",
                args=["--directory", str(path.parent), "run", path.name],
                env=None,
            )
        else:
            server_params = StdioServerParameters(
                command="node",
                args=[server_script_path],
                env=None,
            )

        stdio_transport = await self.exit_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(
            ClientSession(self.stdio, self.write)
        )

        await self.session.initialize()

        response = await self.session.list_tools()
        print("\nConnected to server with tools:")
        for tool in response.tools:
            print(" -", tool.name)

    async def process_query(self, query: str) -> str:
        response = await self.session.list_tools()

        tools = [
            {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema,
            }
            for tool in response.tools
        ]

        chat = self.model.start_chat()

        prompt = f"""
You are an agent with access to tools.

User query:
{query}

Available tools:
{tools}

If a tool is needed, respond ONLY with JSON in this format:
{{
  "tool": "tool_name",
  "args": {{ ... }}
}}

Otherwise, respond normally.
"""

        model_response = chat.send_message(prompt)
        text = model_response.text.strip()

        # Try parsing tool call
        if text.startswith("{") and "tool" in text:
            import json

            call = json.loads(text)
            tool_name = call["tool"]
            tool_args = call.get("args", {})

            result = await self.session.call_tool(tool_name, tool_args)

            followup = f"""
Tool `{tool_name}` returned:
{result.content}

Provide the final answer to the user.
"""
            final_response = chat.send_message(followup)
            return final_response.text

        return text

    async def chat_loop(self):
        print("\nMCP Client (Gemini) started.")
        print("Type 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()
                if query.lower() == "quit":
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print("\nError:", e)

    async def cleanup(self):
        await self.exit_stack.aclose()


async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <server_script>")
        sys.exit(1)

    if not os.getenv("GEMINI_API_KEY"):
        print("Missing GEMINI_API_KEY")
        return

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
