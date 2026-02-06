from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

mcp=FastMCP('weather')

WEATHER_API_KEY = '86a6946ec337426ca5770418231109'
USER_AGENT = 'MCP-Weather-Agent/1.0'

#used to make request:
async def make_request(url:str) -> dict[str,Any] | None :
    headers = {'User-Agent':USER_AGENT,'Accept':'application/geo+json'}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url,headers=headers,timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

#used to format the results:
def format_alert(feature:dict) -> str:
    props = feature['properties']
    return f"""
Event: {props.get("event", "Unknown")}
Area: {props.get("areaDesc", "Unknown")}
Severity: {props.get("severity", "Unknown")}
Description: {props.get("description", "No description available")}
Instructions: {props.get("instruction", "No specific instructions provided")}
"""


@mcp.tool()
async def get_forcast(city:str) -> str:
    weather_url = f'http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no'
    data        = make_request(weather_url)

    if not data:
        return "Unable to fetch weather data."
    
    return data['current']


def main():
    mcp.run(transport='stdio') # This line listens for MCP connections over stdio. stdio means standard input/output.

if __name__ == "__main__":
    main()