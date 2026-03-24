import datetime
from struct_data.state import TravelPlanState
from nodes.get_daily_weather_node import get_daily_weather_node
import asyncio


async def test_get_daily_weather_node():
    """
    测试获取每日天气节点
    """
    # 创建初始状态
    initial_state = TravelPlanState(
        user_id="user1",
        origin_city="上海",
        destination_city="北京",
        travel_dates=(datetime.datetime(2026, 3, 25, 0, 0, 0), datetime.datetime(2026, 3, 28, 23, 59, 59)),
        number_of_days=4,
        number_of_travelers=3,
        age_distribution={'adult': 2, 'child': 1},
        interests=['文化', '自然', '美食'],
        accommodation_preference="酒店"
    )
    
    print("初始状态:")
    print(f"user_id: {initial_state.user_id}")
    print(f"origin_city: {initial_state.origin_city}")
    print(f"destination_city: {initial_state.destination_city}")
    print()
    
    # 调用节点函数
    try:
        updated_state = await get_daily_weather_node(initial_state)
        
        print("更新后的状态:")
        print(f"daily_weather_data: {updated_state.get('daily_weather_data', 'N/A')}")
        print(f"current_step: {updated_state.get('current_step', 'N/A')}")
        print()
            
    except Exception as e:
        print(f"测试失败: {e}")


if __name__ == "__main__":
    asyncio.run(test_get_daily_weather_node())
