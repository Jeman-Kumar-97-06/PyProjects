from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP 

#intialize FastMCP:
app = FastMCP()

#Constants:
NWS_API_URL = "https://api.weather.gov/points/{lat},{lon}/forecast"
USER_AGENT='weather-app/1.0'

async def make_nws_request(url:str) -> dict[str,Any] | None: #The url should be of 'string' type and the function returns a dictionary or None
   headers = {"User-Agent": USER_AGENT,"Accept": "application/geo+json"}
   async with httpx.AsyncClient() as client:
       response = await client.get(url, headers=headers)
       if response.status_code == 200:
           return response.json()
       return None