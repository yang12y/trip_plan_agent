from pydantic import BaseModel, Field
from typing import Dict
from struct_data.state import WeatherInfo


class DailyWeatherData(BaseModel):
    daily_weather_data: Dict[str, WeatherInfo] = Field(default_factory=dict, description="天气信息,包含每天的天气信息，键为YYYY-MM-DD，值为该天的天气信息字典")
   
