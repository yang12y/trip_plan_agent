import asyncio
import sys
import os

from langchain_core.messages import HumanMessage
from struct_data.state import TravelPlanState
from nodes.collection_preferences_node import collect_preferences_node

async def test_collection_preferences_node():
    """
    测试收集用户偏好信息节点
    """
    # 创建初始状态
    initial_state = TravelPlanState(
        user_id="user1",
        messages=[
            HumanMessage(content="从上海去北京，1月1-3日，2成人1小孩，喜欢文化、自然、美食，在酒店住宿，最好做高铁")
        ],
    )
    
    print("初始状态:")
    print(f"user_id: {initial_state.user_id}")
    print(f"messages: {[msg.content for msg in initial_state.messages]}")
    print(f"count: {initial_state.count}")
    print()
    
    # 调用节点函数
    try:
        updated_state = await collect_preferences_node(initial_state)
        
        print("更新后的状态:")
        print(f"user_id: {updated_state.get('user_id', 'N/A')}")
        print(f"origin_city: {updated_state.get('origin_city', 'N/A')}")
        print(f"destination_city: {updated_state.get('destination_city', 'N/A')}")
        print(f"travel_dates: {updated_state.get('travel_dates', 'N/A')}")
        print(f"number_of_days: {updated_state.get('number_of_days', 'N/A')}")
        print(f"number_of_travelers: {updated_state.get('number_of_travelers', 'N/A')}")
        print(f"age_distribution: {updated_state.get('age_distribution', 'N/A')}")
        print(f"interests: {updated_state.get('interests', 'N/A')}")
        print(f"accommodation_preference: {updated_state.get('accommodation_preference', 'N/A')}")
        print(f"count: {updated_state.get('count', 'N/A')}")
        print(f"current_step: {updated_state.get('current_step', 'N/A')}")
        
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_collection_preferences_node())
