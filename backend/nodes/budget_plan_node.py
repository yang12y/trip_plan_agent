from struct_data.state import TravelPlanState, BudgetItem
from agents.budget_plan_agent import get_budget_plan_agent
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
    budget_plan_agent = await get_budget_plan_agent()
    response = await budget_plan_agent.ainvoke({"messages": [user_input]})
    budget_plan = response["structured_response"]
    print(f"预算规划完成，预估总费用：{budget_plan.total_cost}元")
    
    # 更新状态
    state.total_budget = budget_plan.total_cost
    
    # 转换BudgetItem类型
    try:
        budget_items = []
        for item in budget_plan.items:
            # 创建一个新的BudgetItem对象，确保使用正确的类型
            budget_item = BudgetItem(
                category=item.category,
                item_name=item.item_name,
                estimated_cost=item.estimated_cost,
                cost_range=item.cost_range,
                is_essential=item.is_essential,
                save_tips=item.save_tips,
                actual_cost=0.0,
                is_paid=False,
                notes=""
            )
            budget_items.append(budget_item)
        
        state.budget_breakdown = budget_items
    except Exception as e:
        # 如果转换失败，使用空列表
        state.budget_breakdown = []
    
    return state