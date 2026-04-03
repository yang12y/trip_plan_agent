from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from struct_data.state import TravelPlanState
from app.update_trip_graph import update_trip_graph
from data_base.storage import SQLiteStorageService
import asyncio

router = APIRouter(prefix="/update-trip", tags=["update-trip"])


class UpdateTripRequest(BaseModel):
    """更新旅行计划请求模型"""
    user_id: str = Field(description="用户ID")


class UpdateTripResponse(BaseModel):
    """更新旅行计划响应模型"""
    state: str
    data: TravelPlanState


@router.post("/update", response_model=UpdateTripResponse)
async def update_trip(request: UpdateTripRequest):
    """
    更新旅行计划
    """


    # 从数据库中获取旅行计划状态
    storage_service = SQLiteStorageService()
    state = await storage_service.get_state(request.user_id)
    
    if not state:
        raise HTTPException(status_code=404, detail="旅行计划不存在")
    
    try:
        # 执行工作流
        updated_state = await update_trip_graph.ainvoke(state)
        
        # 构建响应
        response = UpdateTripResponse(
            state="success",
            data=updated_state
        )
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"更新旅行计划失败: {str(e)}")
