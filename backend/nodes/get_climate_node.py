from agents.climate_agent import  climate_agent
from struct_data.state import TravelPlanState
from langchain_core.messages import HumanMessage
import datetime



async def get_climate_node(state: TravelPlanState) -> TravelPlanState:
    """
    获取天气节点
    """
    print("开始获取天气信息")

    # 获取今天日期
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    # 计算昨天的日期
    yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    # 构造输入
    input = HumanMessage(content=f"用户位置:{state.destination_city}, 日期: {today}")
    
    # 调用天气智能体
    response = await climate_agent.ainvoke({"messages": [input]})
    
    # 获取结构化信息
    daily_weather_data = response["structured_response"]

    # 判断是否有天气变化（比较今天和昨天的天气）
    is_weather_change = False
    if today in daily_weather_data and yesterday in state.daily_weather_data:
        if daily_weather_data[today] != state.daily_weather_data[yesterday]:
            is_weather_change = True
    elif today in daily_weather_data:
        # 今天有天气信息，昨天没有，视为天气变化
        is_weather_change = True

    print("获取天气信息完成")

    # 更新状态
    return {
        **state.model_dump(),
        "daily_weather_data": daily_weather_data,
        "is_weather_change": is_weather_change
    }
   
