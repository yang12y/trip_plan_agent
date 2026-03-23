from pydantic import BaseModel, Field
from typing import List, Optional, Tuple, Dict
from typing_extensions import Annotated
from operator import add
from struct_data.state import LocationInfo


class AttractionPlan(BaseModel):
    weather_info: Dict[str, dict] = Field(default_factory=dict, description="天气信息,包含旅游从开始时间到结束时间的天气信息")
    attraction_data: Dict[str, dict] = Field(default_factory=dict, description="景点数据,包含推荐景点的详细信息")
