from struct_data.state import TravelPlanState, WeatherInfo
from tools.amap_tools import AmapTools
import datetime
import json


async def get_daily_weather_node(state: TravelPlanState) -> TravelPlanState:
    """
    获取每日天气节点
    直接使用天气工具获取天气信息
    """
    print("开始获取每日天气")

    # 获取当前时间
    current_time = datetime.datetime.now().strftime("%Y-%m-%d")

    # 获取天气工具
    amap_tools = await AmapTools().get_amap_tools()
    weather_tool = None
    for tool in amap_tools:
        if tool.name == "maps_weather":
            weather_tool = tool
            break
    
    if weather_tool is None:
        print("未找到天气工具")
        state.current_step = "get_daily_weather"
        return state

    # 直接调用天气工具
    # 使用目的地城市作为参数
    try:
        response = await weather_tool.ainvoke({"city": state.destination_city})
        
        # 将字符串结果转换为JSON
        if isinstance(response, str):
            weather_data = json.loads(response)
        else:
            weather_data = response
        
        # 解析天气数据
        # 高德地图天气API返回的数据格式：{"city": "北京市", "forecasts": [...]}
        daily_weather = {}
        
        if "forecasts" in weather_data and len(weather_data["forecasts"]) > 0:
            # forecasts直接是天气数据列表
            forecasts = weather_data["forecasts"]
            
            # 只获取第一天的天气数据
            forecast = forecasts[0]
            date = forecast.get("date", "")
            if date:
                # 处理温度字段，可能是字符串，需要转换为浮点数
                daytemp_str = forecast.get("daytemp", "0")
                nighttemp_str = forecast.get("nighttemp", "0")
                daytemp_float_str = forecast.get("daytemp_float", daytemp_str)
                nighttemp_float_str = forecast.get("nighttemp_float", nighttemp_str)
                
                weather_info = WeatherInfo(
                    date=date,
                    week=str(forecast.get("week", "")),
                    dayweather=forecast.get("dayweather", ""),
                    nightweather=forecast.get("nightweather", ""),
                    daytemp=float(daytemp_str) if daytemp_str else 0.0,
                    nighttemp=float(nighttemp_str) if nighttemp_str else 0.0,
                    daywind=forecast.get("daywind", ""),
                    nightwind=forecast.get("nightwind", ""),
                    daypower=forecast.get("daypower", ""),
                    nightpower=forecast.get("nightpower", ""),
                    daytemp_float=float(daytemp_float_str) if daytemp_float_str else 0.0,
                    nighttemp_float=float(nighttemp_float_str) if nighttemp_float_str else 0.0
                )
                daily_weather[date] = weather_info
        
        elif "lives" in weather_data and len(weather_data["lives"]) > 0:
            # 实时天气数据
            live = weather_data["lives"][0]
            date = current_time
            
            temp_str = live.get("temperature", "0")
            
            weather_info = WeatherInfo(
                date=date,
                dayweather=live.get("weather", ""),
                nightweather=live.get("weather", ""),
                daytemp=float(temp_str) if temp_str else 0.0,
                nighttemp=float(temp_str) if temp_str else 0.0,
                daywind=live.get("winddirection", ""),
                nightwind=live.get("winddirection", ""),
                daypower=live.get("windpower", ""),
                nightpower=live.get("windpower", ""),
                daytemp_float=float(temp_str) if temp_str else 0.0,
                nighttemp_float=float(temp_str) if temp_str else 0.0
            )
            daily_weather[date] = weather_info
        
        # 更新状态
        state.daily_weather_data = daily_weather
        print(f"每日天气获取完成，共获取 {len(daily_weather)} 天的天气数据")
        
    except Exception as e:
        print(f"获取天气信息失败: {str(e)}")
        import traceback
        traceback.print_exc()
    
    state.current_step = "get_daily_weather"
    return state
