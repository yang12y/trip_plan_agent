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
    weather_info: Dict[str, dict] = Field(default_factory=dict)
    attraction_data: Dict[str, dict] = Field(default_factory=dict)
    transportation_data: Dict[str, dict] = Field(default_factory=dict)

    # 系统状态
    current_step: str = Field(default="init")
    needs_user_confirmation: bool = Field(default=False)
    pending_modifications: Annotated[List[dict], add] = Field(default_factory=list)



