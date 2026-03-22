import asyncio
from langchain_core.messages import HumanMessage
from struct_data.state import TravelPlanState
from nodes.path_plan_node import path_plan_node
import datetime

async def test_path_plan_node():
    """
    测试路径规划节点
    """
    # 创建初始状态
    initial_state = TravelPlanState(
        user_id="user1",
        messages=[
            HumanMessage(content="从上海去北京，1月1-3日，2成人1小孩，喜欢文化、自然、美食，在酒店住宿，最好做高铁")
        ],
        count=1,
        origin_city="上海",
        destination_city="北京",
        current_step="collect_preferences",
        travel_dates=(datetime.datetime(2025, 1, 1, 0, 0), datetime.datetime(2025, 1, 3, 23, 59, 59)),
        number_of_days=3,
        number_of_travelers=3,
        age_distribution={'adult': 2, 'child': 1},
        interests=['文化', '自然', '美食'],
        accommodation_preference="酒店"
    )
    
    print("初始状态:")
    print(f"user_id: {initial_state.user_id}")
    print(f"origin_city: {initial_state.origin_city}")
    print(f"destination_city: {initial_state.destination_city}")
    print(f"messages: {[msg.content for msg in initial_state.messages]}")
    print(f"count: {initial_state.count}")
    print(f"current_step: {initial_state.current_step}")
    print()
    
    # 调用节点函数
    try:
        updated_state = await path_plan_node(initial_state)
        
        print("更新后的状态:")
        print(f"user_id: {updated_state.get('user_id', 'N/A')}")
        print(f"origin_city: {updated_state.get('origin_city', 'N/A')}")
        print(f"destination_city: {updated_state.get('destination_city', 'N/A')}")
        print(f"driving_trip_path: {updated_state.get('driving_trip_path', 'N/A')}")
        print(f"location_info: {updated_state.get('location_info', 'N/A')}")
        print(f"count: {updated_state.get('count', 'N/A')}")
        print(f"current_step: {updated_state.get('current_step', 'N/A')}")
        print(f"messages: {[msg.content for msg in updated_state.get('messages', [])]}")
        
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_path_plan_node())
