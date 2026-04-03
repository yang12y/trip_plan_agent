from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from struct_data.state import TravelPlanState
from langchain_core.messages import HumanMessage, AIMessage
from app.trip_plan_graph import trip_plan_graph
import asyncio

from data_base.storage import SQLiteStorageService

router = APIRouter(prefix="/trip-plan", tags=["trip-plan"])

class TripPlanRequest(BaseModel):
    """旅行计划请求模型"""
    user_id: str = Field(description="用户 ID")
    message: str = Field(description="旅行计划请求消息")
    budget: float = Field(description="预算")

class TripPlanResponse(BaseModel):
    """旅行计划响应模型"""
    state: str = Field(default="success", description="是否响应成功")
    data: TravelPlanState = Field(description="旅行计划状态")


@router.post("/create", response_model=TripPlanResponse)
async def create_trip_plan(request: TripPlanRequest):
    """
    创建旅行计划
    
    - **user_id**: 用户 ID
    - **message**: 旅行计划请求消息，格式如："从南昌去上海，2026年1月12成人1小孩2成人1小孩，喜欢文化、自然、美食，在酒店住宿，最好做高铁"
    - **budget**: 预算，单位为元
    """
    try:
        # 创建初始状态
        print("创建初始状态")
        initial_state = TravelPlanState(
            user_id=request.user_id,
            messages=[HumanMessage(content=request.message)],
            total_budget=request.budget
        )
        
        # 执行工作流
        print("执行工作流")
        updated_state = await trip_plan_graph.ainvoke(initial_state)
        print(f"工作流执行完成，updated_state类型: {type(updated_state)}")
        
        # 确保updated_state是TravelPlanState对象
        if isinstance(updated_state, dict):
            print("转换字典为TravelPlanState对象")
            # 处理messages字段，确保它是正确的格式
            if "messages" in updated_state:
                messages = []
                for msg in updated_state["messages"]:
                    if isinstance(msg, dict):
                        if msg.get("type") == "HumanMessage":
                            messages.append(HumanMessage(content=msg.get("content", "")))
                        elif msg.get("type") == "AIMessage":
                            messages.append(AIMessage(content=msg.get("content", "")))
                updated_state["messages"] = messages
            # 转换为TravelPlanState对象
            updated_state = TravelPlanState(**updated_state)
        
        # 构建响应
        print("构建响应")
        response = TripPlanResponse(
            state="success",
            data=updated_state
        )
        print("响应构建完成")
        
        return response

    except Exception as e:
        print(f"创建旅行计划失败: {str(e)}")
        import traceback
        traceback.print_exc()
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
