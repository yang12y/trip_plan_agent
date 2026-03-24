from pydantic import BaseModel, Field
from typing import Dict
from struct_data.state import WeatherInfo


class DailyWeatherData(BaseModel):
    daily_weather_data: Dict[str, WeatherInfo] = Field(default_factory=dict, description="每日天气数据")
   
