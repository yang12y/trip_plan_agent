from langchain_core.messages import HumanMessage
from agents.update_plan import get_update_plan_agent
from struct_data.state import TravelPlanState
from datetime import datetime


async def update_plan_node(state: TravelPlanState) -> TravelPlanState:
    """
    更新用户的旅游计划
    :param state: 包含用户信息和旅游计划的状态
    :return: 包含更新后的旅游计划的状态
    """
    print("开始更新旅游计划")

    # 获取今天日期
    today = datetime.now().strftime("%Y-%m-%d")

    # 构造用户输入
    user_input = HumanMessage(
        content=f"""
        今天日期为{today},
        我的结束日期为{state.travel_dates[1].strftime('%Y年%m月%d日')},
        我的旅游人数构成为{state.number_of_travelers},
        我的住宿偏好为{state.accommodation_preference},
        我的兴趣偏好为{state.interests},
        我的目的地为{state.destination_city},
        因为天气变故，请你根据最新的天气信息更新我的旅游计划。
        """
    )

    # 调用更新计划助手
    update_plan_agent = get_update_plan_agent()
    response = await update_plan_agent.ainvoke({"messages": [user_input]})

    # 获取结构化输出
    updated_plan = response["structured_response"]
    print(updated_plan)

    # 更新状态
    attraction_data = state.attraction_data.copy()
    if hasattr(updated_plan, 'attraction_data') and updated_plan.attraction_data:
        # 只更新存在的日期，保留原有日期
        for date, attractions in updated_plan.attraction_data.items():
            if date in attraction_data:
                # 更新该日期的景点
                attraction_data[date].update(attractions)
            else:
                # 添加新日期的景点
                attraction_data[date] = attractions
    
    weather_info = state.weather_info.copy()
    if hasattr(updated_plan, 'weather_info') and updated_plan.weather_info:
        # 只更新存在的日期，保留原有日期
        for date, weather in updated_plan.weather_info.items():
            if date in weather_info:
                # 更新该日期的天气
                weather_info[date] = weather
            else:
                # 添加新日期的天气
                weather_info[date] = weather

    print("更新旅游计划完成")

    return {
        **state.model_dump(),
        "attraction_data": attraction_data,
        "weather_info": weather_info,
    }





