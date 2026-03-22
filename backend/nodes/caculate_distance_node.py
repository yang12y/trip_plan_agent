from struct_data.state import TravelPlanState
from tools.amap_tools import AmapTools
from struct_data.state import LocationInfo
from langchain_core.messages import HumanMessage
import datetime
import json



import asyncio

async def caculate_distance_node(state: TravelPlanState) -> TravelPlanState:
    """
    计算行程距离
    """
    print("正在计算行程距离")
    # 获取旅行基本信息
    origin_city = state.origin_city
    destination_city = state.destination_city

    # 获取高德地图工具，包括地理编码工具和距离计算工具
    amap_tools = await AmapTools().get_amap_tools()
    for tool in amap_tools:
        if tool.name == "maps_geo":
            geo_tool = tool
        elif tool.name == "maps_distance":
            driving_tool = tool

    # 调用地理编码工具获取城市经纬度
    origin_coords_str = await geo_tool.ainvoke({"address": origin_city})
    origin_coords = json.loads(origin_coords_str).get("return")[0].get("location")  if origin_coords_str else None
    
    destination_coords_str = await geo_tool.ainvoke({"address": destination_city})
    destination_coords = json.loads(destination_coords_str).get("return")[0].get("location")  if destination_coords_str else None
    
    location_info = LocationInfo(
        origin_location=origin_coords,
        destination_location=destination_coords,
    )
    
    # 调用距离计算工具计算距离
    distance = await driving_tool.ainvoke({"origins": origin_coords,
        "destination": destination_coords,
        "type": "0"})
    distance = json.loads(distance).get("results")[0].get("distance", 0.0)

    print(f"计算得到的行程距离为：{distance}米")
    print(f"转换为公里：：{float(distance)/1000}公里")
    print("计算行程距离完成")
    
    return {
        **state.model_dump(),  # 包含所有状态字段
        "location_info": location_info,  # 包含计算得到的位置信息字段
        "distance": float(distance)/1000,  # 包含计算得到的距离字段
    }

if __name__ == "__main__":
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
    
    asyncio.run(caculate_distance_node(initial_state))
