from agents.path_plan_agent import path_plan_agent
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from struct_data.state import TravelPlanState


async def path_plan_node(state: TravelPlanState) -> TravelPlanState:
    """
    计划行程
    """
    print("正在计划行程") 
    # 获取旅行基本信息
    origin_city = state.origin_city
    destination_city = state.destination_city

    # 初始化用户输入
    user_input = HumanMessage(content=f"计划从{origin_city}到{destination_city}的行程")

    # 路径规划智能体执行
    try:
        response = await path_plan_agent.ainvoke({"messages": [user_input]})

        # 从模型返回的结构化响应中提取路径规划信息
        path_plan = response["structured_response"]

        # 从模型返回结果提取AI的回复
        ai_content = response["messages"][-1].content
        ai_msg = AIMessage(content=ai_content)
        print("计划行程完成")

        # 更新状态
        return {
            **state.model_dump(),
            **path_plan.model_dump(exclude_unset=True),
            "messages": [user_input, ai_msg],
            "count": state.count + 1,
            "current_step": "path_plan",
            "steps": ["path_plan"],
        }
    except Exception as e:
        print(f"路径规划失败: {e}")
        # 返回一个包含错误信息的状态
        return {
            **state.model_dump(),
            "messages": [user_input, AIMessage(content=f"路径规划失败: {str(e)}")],
            "count": state.count + 1,
            "current_step": "error",
            "error_message": str(e)
        }
   
