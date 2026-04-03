from nodes.get_daily_weather_node import get_daily_weather_node
from fastapi import APIRouter,HTTPException
from struct_data.daily_weather import DailyWeatherData
from data_base.storage import SQLiteStorageService
from pydantic import BaseModel,Field


router = APIRouter(prefix="/weather", tags=["weather"])


class WeatherRequest(BaseModel):
    user_id: str = Field(description="用户ID")

class WeatherResponse(BaseModel):
    daily_weather_data: DailyWeatherData = Field(description="目的地天气信息")


@router.post("/get", response_model=WeatherResponse)
async def get_destination_weather(request:WeatherRequest):
    """
    获取目的地天气信息
    """
    # 从数据库中获取旅行计划状态
    storage_service = SQLiteStorageService()
    state = storage_service.get_state(request.user_id)
    
    if not state:
        raise HTTPException(status_code=404, detail="旅行计划不存在")
    
    # 调用天气节点
    state = await get_daily_weather_node(state)
    
    # 返回天气信息
    return WeatherResponse(daily_weather_data=DailyWeatherData(daily_weather_data=state.daily_weather_data))
    
