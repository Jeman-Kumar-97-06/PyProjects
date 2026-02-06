from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")

WEATHER_API_KEY = "86a6946ec337426ca5770418231109"
USER_AGENT = "MCP-Weather-Agent/1.0"


async def make_request(url: str) -> dict[str, Any] | None:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print("Weather API error:", e)
            return None


@mcp.tool()
async def get_forecast(city: str) -> str:
    """
    Get current weather for a city.
    """
    weather_url = (
        f"http://api.weatherapi.com/v1/current.json"
        f"?key={WEATHER_API_KEY}&q={city}&aqi=no"
    )

    data = await make_request(weather_url)

    if not data or "current" not in data:
        return "Unable to fetch weather data."

    current = data["current"]

    # 🔑 RETURN TEXT, NOT DICT
    return (
        f"Temperature: {current['temp_c']}°C\n"
        f"Condition: {current['condition']['text']}\n"
        f"Humidity: {current['humidity']}%\n"
        f"Wind: {current['wind_kph']} kph"
    )


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
