from pydantic import BaseModel, Field
from typing import List, Optional, Tuple, Dict
from typing_extensions import Annotated
from operator import add
from struct_data.state import AttractionInfo, WeatherInfo


class AttractionPlan(BaseModel):
    attraction_data: Dict[str, dict[str,AttractionInfo]] = Field(default_factory=dict, description="景点数据,包含每天推荐游玩的景点的详细信息")
    weather_info: Dict[str, WeatherInfo] = Field(default_factory=dict, description="天气信息,包含每天的天气信息")
   
