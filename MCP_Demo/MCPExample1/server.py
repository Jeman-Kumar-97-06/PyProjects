from mcp.server.fastmcp from FastMCP

#initialize the server:
mcp = FastMCP("Weather Service")

#Define a tool using the decorator:
@mcp.tool()
def get_weather(city:str) -> str:
    city = city.lower().strip()
    weather_data = {
        "new york": "Sunny, 25°C",
        "los angeles": "Cloudy, 22°C",
        "chicago": "Rainy, 18°C",
        "miami": "Sunny, 30°C",
    }
    return weather_data.get(city, "Weather data not available for this city.")
    
if __name__ == "__main__":
    mcp.run()