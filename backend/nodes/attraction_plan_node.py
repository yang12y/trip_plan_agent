from struct_data.state import TravelPlanState
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from agents.attraction_plan_agent import attraction_plan_agent

async def attraction_plan_node(state: TravelPlanState) -> TravelPlanState:
    """
    景点推荐节点
    """

    # 构造用户输入
    user_input = HumanMessage(
        content=f"我要从{state.origin_city}到{state.destination_city}的旅游,旅游时间为{state.travel_dates},请你帮我推荐适合的景点"
    )
    
    # 调用景点推荐助手
    response = await attraction_plan_agent.ainvoke(user_input)

    # 提取结构化信息
    attraction_plan = response["structured_response"]

    # 提取AI回复
    ai_content = response["messages"][-1].content
    ai_msg = AIMessage(content=ai_content)
    
    # 更新状态
    return {
        **state.model_dump(),
        **attraction_plan.model_dump(exclude_unset=True),
        "messages": [user_input, ai_msg],
        "count": state.count + 1,
        "current_step": "attraction_plan",
        "steps": ["attraction_plan"],
    }