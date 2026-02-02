from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather Service")

@mcp.tool()
def get_weather(location: str) -> str:
    # localtion should be a string and the return value should also be a string
    # we are going to get the weather of the given location
    city = location.lower().strip()

    weather_data = {
        "new york": "Sunny, 25°C",
        "los angeles": "Cloudy, 22°C",
        "chicago": "Rainy, 18°C",
        "miami": "Sunny, 30°C", 
    }
    return weather_data.get(city, "Weather data not available for this location.")

if __name__ == "__main__":
    mcp.run()