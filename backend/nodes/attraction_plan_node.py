from struct_data.state import TravelPlanState, AttractionInfo, WeatherInfo
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from agents.attraction_plan_agent import get_attraction_plan_agent

async def attraction_plan_node(state: TravelPlanState) -> TravelPlanState:
    """
    景点推荐节点
    """
    print("开始景点推荐")

    # 格式化 travel_dates 为字符串
    start_date = state.travel_dates[0].strftime("%Y年%m月%d日")
    end_date = state.travel_dates[1].strftime("%Y年%m月%d日")
    travel_dates_str = f"{start_date}-{end_date}"
    print(travel_dates_str)

    # 构造用户输入
    user_input = HumanMessage(
        content=f"""我要去{state.destination_city}的旅游。
        时间：{travel_dates_str},
        旅行人员构成：{state.age_distribution},
        住宿：{state.accommodation_preference},
        兴趣偏好：{state.interests},
        """
    )
    
    # 调用景点推荐助手
    attraction_plan_agent = await get_attraction_plan_agent()
    response = await attraction_plan_agent.ainvoke({"messages": [user_input]})

    # 获取结构化输出
    attraction_data = response["structured_response"]
    
    # 提取AI回复
    ai_content = response["messages"][-1].content
    ai_msg = AIMessage(content=ai_content)

    print("景点推荐完成")
    
    # 更新状态
    for key, value in attraction_data.model_dump(exclude_unset=True).items():
        if key == "weather_info" and isinstance(value, dict):
            # 转换weather_info中的字典为WeatherInfo对象
            weather_info = {}
            for date, weather_dict in value.items():
                weather_info[date] = WeatherInfo(**weather_dict)
            setattr(state, key, weather_info)
        elif key == "attraction_data" and isinstance(value, dict):
            # 转换attraction_data中的字典为AttractionInfo对象
            attraction_data_dict = {}
            for date, attractions in value.items():
                attraction_data_dict[date] = {}
                for attraction_name, attraction_dict in attractions.items():
                    attraction_data_dict[date][attraction_name] = AttractionInfo(**attraction_dict)
            setattr(state, key, attraction_data_dict)
        else:
            setattr(state, key, value)
    state.messages = [user_input, ai_msg]
    state.count = state.count + 1
    state.current_step = "attraction_plan"
    state.steps = ["attraction_plan"]
    
    return state