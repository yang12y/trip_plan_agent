import datetime
from struct_data.state import TravelPlanState
from data_base.storage import SQLiteStorageService


def test_sqlite_storage():
    """
    测试 SQLite 存储服务
    """
    # 创建存储服务实例
    storage = SQLiteStorageService()
    
    # 创建测试用户 ID
    test_user_id = "test_user_123"
    
    # 创建测试状态
    test_state = TravelPlanState(
        user_id=test_user_id,
        origin_city="上海",
        destination_city="北京",
        travel_dates=(datetime.datetime(2026, 3, 24, 0, 0, 0), datetime.datetime(2026, 3, 27, 23, 59, 59)),
        number_of_days=4,
        number_of_travelers=3,
        age_distribution={'adult': 2, 'child': 1},
        interests=['文化', '自然', '美食'],
        accommodation_preference="酒店",
        weather_info={
            '2026-03-24': {
                'date': '2026-03-24',
                'week': '2',
                'dayweather': '晴',
                'nightweather': '晴',
                'daytemp': 20.0,
                'nighttemp': 7.0,
                'daywind': '南',
                'nightwind': '南',
                'daypower': '1-3',
                'nightpower': '1-3',
                'daytemp_float': 20.0,
                'nighttemp_float': 7.0
            }
        }
    )
    
    print("测试保存状态...")
    # 保存状态
    storage.save_state(test_user_id, test_state)
    print("状态保存成功")
    
    print("\n测试获取状态...")
    # 获取状态
    retrieved_state = storage.get_state(test_user_id)
    if retrieved_state:
        print("状态获取成功")
        print(f"用户 ID: {retrieved_state.user_id}")
        print(f"出发城市: {retrieved_state.origin_city}")
        print(f"目的地城市: {retrieved_state.destination_city}")
        print(f"旅行日期: {retrieved_state.travel_dates}")
        print(f"天气信息: {retrieved_state.weather_info}")
    else:
        print("状态获取失败")
    
    print("\n测试列出用户...")
    # 列出所有用户
    users = storage.list_users()
    print(f"用户列表: {users}")
    
    print("\n测试删除状态...")
    # 删除状态
    storage.delete_state(test_user_id)
    print("状态删除成功")
    
    # 验证状态已删除
    deleted_state = storage.get_state(test_user_id)
    if not deleted_state:
        print("状态删除验证成功")
    else:
        print("状态删除验证失败")
    
    print("\n所有测试完成！")


if __name__ == "__main__":
    test_sqlite_storage()
