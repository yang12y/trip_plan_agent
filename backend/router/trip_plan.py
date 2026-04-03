from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from struct_data.state import TravelPlanState
from langchain_core.messages import HumanMessage
from app.trip_plan_graph import trip_plan_graph
import asyncio

from data_base.storage import SQLiteStorageService

router = APIRouter(prefix="/trip-plan", tags=["trip-plan"])

class TripPlanRequest(BaseModel):
    """旅行计划请求模型"""
    user_id: str
    message: str
    budget: float = 0.0
    currency: str = "CNY"

class TripPlanResponse(BaseModel):
    """旅行计划响应模型"""
    state: str
    data: TravelPlanState


@router.post("/create", response_model=TripPlanResponse)
async def create_trip_plan(request: TripPlanRequest):
    """
    创建旅行计划
    
    - **user_id**: 用户 ID
    - **message**: 旅行计划请求消息，格式如："从南昌去上海，2026年1月1-3日，2成人1小孩，喜欢文化、自然、美食，在酒店住宿，最好做高铁"
    """
    try:
        # 创建初始状态
        initial_state = TravelPlanState(
            user_id=request.user_id,
            messages=[HumanMessage(content=request.message)],
            total_budget=request.budget,
            currency=request.currency
        )
        
        # 执行工作流
        updated_state = await trip_plan_graph.ainvoke(initial_state)
        
        # 构建响应
        response = TripPlanResponse(
            state="success",
            data=updated_state
        )
        
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建旅行计划失败: {str(e)}")


@router.get("/status/{user_id}", response_model=TripPlanResponse)
async def get_trip_plan_status(user_id: str):
    """
    获取旅行计划状态
    
    - **user_id**: 用户 ID
    """
    try:
        # 从数据库中获取用户的旅行计划状态
        storage = SQLiteStorageService()
        response = storage.get_state(user_id)

        if response is None:
            raise HTTPException(status_code=404, detail="旅行计划不存在")
        
        # 构建响应
        return TripPlanResponse(
            state="success",
            data=response
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取旅行计划状态失败: {str(e)}")
