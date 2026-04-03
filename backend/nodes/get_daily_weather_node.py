from struct_data.state import TravelPlanState
from agents.climate_agent import get_climate_agent
import datetime
from langchain_core.messages import HumanMessage

async def get_daily_weather_node(state: TravelPlanState) -> TravelPlanState:
    """
    获取每日天气节点
    """
    print("开始获取每日天气")

    # 获取当前时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d")

    # 构造用户输入
    user_input = HumanMessage(content=f"请获取{state.destination_city}的{current_time}的天气信息")

    # 调用天气智能体获取每日天气
    climate_agent = get_climate_agent()
    response = await climate_agent.ainvoke({"messages": [user_input]})

    # 获取结构化输出
    daily_weather_data = response["structured_response"]
    print("每日天气获取完成")

    return {
        **state.model_dump(),
        **daily_weather_data.model_dump(exclude_unset=True),
        "current_step": "get_daily_weather",
    }