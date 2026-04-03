from agents.collect_preferences_agent import collect_preferences_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from struct_data.state import TravelPlanState
from utils.edit_date import adjust_end_time


async def collect_preferences_node(state: TravelPlanState) -> TravelPlanState:
    """
    收集用户的旅游信息
    """
    print("正在收集用户的旅游信息")

    user_input = state.messages[-1].content
    response = await collect_preferences_agent.ainvoke(
        {
            "messages": state.messages[-3:] + [HumanMessage(content=user_input)]
        }
    )
    # 从模型返回的结构化响应中提取偏好信息
    preferences = response["structured_response"]
    # print(f"preferences: {preferences}")
    # 调整结束时间为当天的23:59:59
    preferences.travel_dates = adjust_end_time(preferences.travel_dates)
    # 计算旅行天数
    preferences.number_of_days = (preferences.travel_dates[1] - preferences.travel_dates[0]).days + 1
    
    # 从模型返回结果提取AI的回复
    ai_content = response["messages"][-1].content
    ai_msg = AIMessage(content=ai_content)
    print("收集用户的旅游信息完成")

    # 更新状态
    for key, value in preferences.model_dump(exclude_unset=True).items():
        setattr(state, key, value)
    state.messages = [ai_msg]
    state.count = state.count + 1
    state.current_step = "collect_preferences"
    state.steps = ["collect_preferences"]
    
    return state
