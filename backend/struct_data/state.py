from pydantic import BaseModel, Field
from typing import List, Optional, Tuple, Dict
from typing_extensions import Annotated
from operator import add 
from datetime import datetime
from typing import Any  # For dict flexibility
from langchain_core.messages import BaseMessage

def merge_dicts(left: Dict[str, Any], right: Dict[str, Any]) -> Dict[str, Any]:
    """合并两个字典，优先考虑右侧字典的值"""
    return {**left, **right}

class LocationInfo(BaseModel):
    origin_location: str = Field(default="", description="Starting location")
    destination_location: str = Field(default="", description="Destination location")


class AttractionInfo(BaseModel):
    attraction_name: str = Field(default="", description="景点名称")
    attraction_location: str = Field(default="", description="景点位置")
    attraction_type: str = Field(default="", description="景点类型")
    attraction_description: str = Field(default="", description="景点描述")
    attraction_price: float | None = Field(default=None, description="景点价格")
    attraction_time: str = Field(default="", description="景点开放时间")
    attraction_adapt_person: str = Field(default="", description="景点的适合人群")
    attraction_special: str = Field(default="", description="景点的特色")
    attraction_play_time_range: str = Field(default="", description="景点的建议游玩时间")
    attraction_score: int = Field(default=0, description="景点的评分")

class WeatherInfo(BaseModel):
    date: str = Field(default="", description="日期，格式为 YYYY-MM-DD")
    week: str = Field(default="", description="星期几，1 表示周一，2 表示周二，以此类推")
    dayweather: str = Field(default="", description="白天的天气状况")
    nightweather: str = Field(default="", description="晚上 的天气状况")
    daytemp: float = Field(default=0.0, description="白天的温度，单位为摄氏度")
    nighttemp: float = Field(default=0.0, description="晚上 的温度，单位为摄氏度")
    daywind: str = Field(default="", description="白天的风向")
    nightwind: str = Field(default="", description="晚上的风向")
    daypower: str = Field(default="", description="白天风力等级")
    nightpower: str = Field(default="", description="晚上的风力等级")
    daytemp_float: float = Field(default=0.0, description="白天温度的浮点表示")
    nighttemp_float: float = Field(default=0.0, description="晚上的温度的浮点表示")



class TravelPlanState(BaseModel):
    user_id: str

    # 多轮对话历史管理
    messages: Annotated[List[BaseMessage], add] = Field(default_factory=list)
    count: int = Field(default=0)

    # 旅行基本信息
    origin_city: str = Field(default="", description="Starting city")
    destination_city: str = Field(default="", description="Destination city")
    travel_dates: Tuple[datetime, datetime] = Field(default=(datetime.now(), datetime.now()), description="Travel dates")
    number_of_days: int = Field(default=0)
    number_of_travelers: int = Field(default=0)
    age_distribution: Annotated[Dict[str, int], merge_dicts] = Field(default_factory=dict)

    # 预算信息
    total_budget: float = Field(default=0.0)
    budget_breakdown: Annotated[Dict[str, float], merge_dicts] = Field(default_factory=dict)

    # 兴趣偏好
    interests: List[str] = Field(default_factory=list)
    accommodation_preference: str = Field(default="")
    special_requirements: List[str] = Field(default_factory=list)

    # 行程信息
    bicycling_trip_path: Annotated[List[dict], add] = Field(default_factory=list)
    location_info: LocationInfo = Field(default_factory=LocationInfo)
    walking_trip_path: Annotated[List[dict], add] = Field(default_factory=list)
    driving_trip_path: Annotated[List[dict], add] = Field(default_factory=list)
    transit_integrated_trip_path: Annotated[List[dict], add] = Field(default_factory=list)
    distance: float = Field(default=0.0)

    # 实时数据
    weather_info: Dict[str, WeatherInfo] = Field(default_factory=dict)
    attraction_data: Dict[str, dict[str,AttractionInfo]] = Field(default_factory=dict)
    transportation_data: Dict[str, dict] = Field(default_factory=dict)
    daily_weather_data: Dict[str, WeatherInfo] = Field(default_factory=dict)

    # 系统状态
    current_step: str = Field(default="init")
    steps: Annotated[List[str], add] = Field(default_factory=list)
    needs_user_confirmation: bool = Field(default=False)
    pending_modifications: Annotated[List[dict], add] = Field(default_factory=list)



