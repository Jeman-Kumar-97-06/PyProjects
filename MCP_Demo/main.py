'''
MCP Server Quickstart Demo
'''

from mcp.server.mcpserver import MCPServer

mcp = MCPServer('Demo')

@mcp.tool()
def add(a:int, b:int) -> int:
    return a + b

@mcp.resource("greeting://{name}")
def get_greeting(name:str) -> str:
    return f"Hello {name}!"

@mcp.prompt()
def greet_user(name:str, style:str = 'friendly')->str:
    styles= {
        "friendly":"Please write a warm, friendly greeting",
        "formal"  :"Please write a formal, professional greeting",
        "casual"  :"Please write a casual, relaxed greeting"
    }

def main():
    print("Hello from mcp-demo!")


if __name__ == "__main__":
    main()
