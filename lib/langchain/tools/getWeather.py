from pydantic.v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import Optional, Type

class WeatherToolCheckInput(BaseModel):
    """Input for City and temperature unit, for get the current weather"""

    city: str = Field(..., description="The city that user wants to see the weather. For example: London")
    temperatureUnit: str = Field(..., description="The temperature unit. For example: celsius")

class WeatherTool(BaseTool):
    name="get_weather_tool"
    description="Useful for when you need get the current weather for an specify city. For example: The city and state, e.g. San Francisco, CA"

    def _run(self, city:str, temperatureUnit: str):
        result = print(f"The weather for {city} is: {temperatureUnit}")
        return result
    def _arun(self, city:str, temperatureUnit: str):
        raise NotImplementedError("This tool does not support async")
    
    args_schema: Optional[Type[BaseModel]] = WeatherToolCheckInput
