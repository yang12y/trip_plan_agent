import datetime
from struct_data.state import TravelPlanState, WeatherInfo, AttractionInfo
from struct_data.attraction_plan import AttractionPlan
from nodes.update_plan_node import update_plan


async def test_update_plan():
    """
    测试更新旅游计划节点
    """
    # 创建测试状态
    initial_state = TravelPlanState(
        user_id="user1",
        origin_city="南昌",
        destination_city="上海",
        travel_dates=(datetime.datetime(2026, 3, 24, 0, 0, 0), datetime.datetime(2026, 3, 25, 23, 59, 59)),
        number_of_days=3,
        number_of_travelers=3,
        age_distribution={'adult': 2, 'child': 1},
        interests=['文化', '自然', '美食'],
        accommodation_preference="酒店",
        attraction_data={
            '2026-03-24': {
                '外滩': AttractionInfo(
                    attraction_name='外滩',
                    attraction_location='中山东一路',
                    attraction_time='全天',
                    attraction_play_time_range='2小时'
                )
            },
            '2026-03-25': {
                '上海博物馆': AttractionInfo(
                    attraction_name='上海博物馆',
                    attraction_location='人民大道201号',
                    attraction_time='9:00-17:00',
                    attraction_play_time_range='3小时'
                )
            }
        },
        weather_info={
            '2026-03-24': WeatherInfo(
                date='2026-03-24',
                week='4',
                dayweather='晴',
                nightweather='晴',
                daytemp=10.0,
                nighttemp=5.0,
                daywind='北',
                nightwind='北',
                daypower='1-3',
                nightpower='1-3',
                daytemp_float=10.0,
                nighttemp_float=5.0
            ),
            '2026-03-25': WeatherInfo(
                date='2026-03-25',
                week='5',
                dayweather='小雨',
                nightweather='阴',
                daytemp=8.0,
                nighttemp=4.0,
                daywind='东北',
                nightwind='东北',
                daypower='1-3',
                nightpower='1-3',
                daytemp_float=8.0,
                nighttemp_float=4.0
            )
        },
    )
    
    print("初始状态:")
    print(f"用户 ID: {initial_state.user_id}")
    print(f"目的地城市: {initial_state.destination_city}")
    print(f"旅行日期: {initial_state.travel_dates}")
    print(f"初始景点数据: {initial_state.attraction_data}")
    print(f"初始天气信息: {initial_state.weather_info}")
    print()
    
    # 调用更新计划函数
    try:
        updated_state = await update_plan(initial_state)
        
        print("更新后的状态:")
        print(f"用户 ID: {updated_state.get('user_id', 'N/A')}")
        print(f"目的地城市: {updated_state.get('destination_city', 'N/A')}")
        print(f"更新后的景点数据: {updated_state.get('attraction_data', 'N/A')}")
        print(f"更新后的天气信息: {updated_state.get('weather_info', 'N/A')}")
        print()
        
        # 验证更新是否成功
        if 'attraction_data' in updated_state and updated_state['attraction_data']:
            print("测试通过: 成功更新旅游计划")
        else:
            print("测试失败: 未更新旅游计划")
            
    except Exception as e:
        print(f"测试失败: {e}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(test_update_plan())
    
