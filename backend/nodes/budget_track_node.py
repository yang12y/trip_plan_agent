from struct_data.state import TravelPlanState, BudgetItem

def update_budget_actual(state: TravelPlanState, item_name: str, actual_cost: float) -> TravelPlanState:
    """
    更新实际花费
    """
    budget_breakdown = state.budget_breakdown.copy()
    
    for item in budget_breakdown:
        if item.item_name == item_name:
            item.actual_cost = actual_cost
            item.is_paid = True
            break
    else:
        # 如果找不到，添加新项目
        budget_breakdown.append(BudgetItem(
            category="其他",
            item_name=item_name,
            actual_cost=actual_cost,
            is_paid=True
        ))
    
    return {
        **state.model_dump(),
        "budget_breakdown": budget_breakdown,
    }

def get_budget_status(state: TravelPlanState) -> dict:
    """
    获取预算执行情况
    """
    total_estimated = sum(item.estimated_cost for item in state.budget_breakdown)
    total_actual = sum(item.actual_cost for item in state.budget_breakdown)
    remaining = state.total_budget - total_actual
    
    return {
        "总预算": state.total_budget,
        "预估总费用": total_estimated,
        "实际已花费": total_actual,
        "剩余预算": remaining,
        "执行进度": f"{(total_actual/total_estimated)*100:.1f}%" if total_estimated > 0 else "0%",
        "是否超支": total_actual > state.total_budget,
    }