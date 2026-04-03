from struct_data.state import TravelPlanState, BudgetItem
from agents.budget_plan_agent import budget_plan_agent
from langchain_core.messages import HumanMessage

async def budget_plan_node(state: TravelPlanState) -> TravelPlanState:
    """
    预算规划节点
    根据行程规划生成详细的预算清单
    """
    print("开始预算规划")
    
    # 构造用户输入
    user_input = HumanMessage(
        content=f"""
        目的地：{state.destination_city}
        天数：{state.number_of_days}天
        人数：{state.number_of_travelers}人
        交通方式：{state.transportation_data}
        住宿偏好：{state.accommodation_preference}
        景点计划：{state.attraction_data}
        
        请为这次旅行生成详细的预算规划。
        """
    )
    
    # 调用预算规划智能体
    response = await budget_plan_agent.ainvoke({"messages": [user_input]})
    budget_plan = response["structured_response"]
    
    print(f"预算规划完成，预估总费用：{budget_plan.total_cost}元")
    
    return {
        **state.model_dump(),
        "total_budget": budget_plan.total_cost,
        "budget_breakdown": budget_plan.items,
    }