import asyncio
from tools.amap_tools import AmapTools
import json

async def call_amap_tools():
    # 初始化AmapTools并获取工具列表
    amap_tools = AmapTools()
    tools = await amap_tools.get_amap_tools()
    
    # 1. 查找工具（示例：地理编码工具）
    geo_tool = None
    driving_tool = None
    for tool in tools:
        if tool.name == "maps_geo":
            geo_tool = tool
        elif tool.name == "maps_direction_driving":
            driving_tool = tool
        elif tool.name == "maps_weather":
            weather_tool = tool
    
    if geo_tool and driving_tool and weather_tool:
        # 2. 调用地理编码工具（将地址转换为经纬度）
        geo_result = await geo_tool.ainvoke({
            "address": "北京市海淀区中关村",
            "city": "北京"
        })
        print("地理编码结果类型:", type(json.loads(geo_result)))
        """
        {
            "return": [
                {
                "country": "中国",
                "province": "北京市",
                "city": "北京市",
                "citycode": "010",
                "district": "海淀区",
                "street": [],
                "number": [],
                "adcode": "110108",
                "location": "116.326423,39.980618",
                "level": "住宅区"
                }
            ]
        }
        """
        
        # 假设地理编码返回了经纬度（示例值）
        beijing_location = "116.319895,39.959865"  # 中关村经纬度
        shanghai_location = "121.473701,31.230416"  # 上海外滩经纬度
        
        # 3. 调用驾车路径规划工具
        driving_result = await driving_tool.ainvoke({
            "origin": shanghai_location,
            "destination": beijing_location
        })
        print("驾车路径规划结果类型:", type(json.loads(driving_result)))
        """
        {
            "route": {
                "origin": "121.473701,31.230416",
                "destination": "116.319895,39.959865",
                "paths": [
                    {
                        "distance": "1231986",
                        "duration": "48953",
                        "steps": [
                            {
                                "instruction": "向西行驶43米左转",
                                "distance": "43",
                                "orientation": "西",
                                "duration": "19"
                            },
                            {
                                "instruction": "向西南行驶77米左转",
                                "distance": "77",
                                "orientation": "西南",
                                "duration": "23"
                            }
                        ]
                    }
                ]
            }
        }
        """


async def call_weather_tool():
    # 初始化AmapTools并获取工具列表
    amap_tools = AmapTools()
    tools = await amap_tools.get_amap_tools()
    
    # 1. 查找工具（示例：天气工具）
    weather_tool = None
    for tool in tools:
        if tool.name == "maps_weather":
            weather_tool = tool
    
    if weather_tool:
        # 2. 调用天气工具
        weather_result = await weather_tool.ainvoke({
            "city": "北京",
        })
        print(weather_result)
        print("天气结果类型:", type(json.loads(weather_result)))    #天气结果类型: <class 'dict'>
        {
            "city": "北京市",
            "forecasts": [
                {
                    "date": "2026-03-22",
                    "week": "7",
                    "dayweather": "晴",
                    "nightweather": "多云",
                    "daytemp": "22",
                    "nighttemp": "7",
                    "daywind": "北",
                    "nightwind": "北",
                    "daypower": "1-3",
                    "nightpower": "1-3",
                    "daytemp_float": "22.0",
                    "nighttemp_float": "7.0"
                },
                {
                    "date": "2026-03-23",
                    "week": "1",
                    "dayweather": "多云",
                    "nightweather": "晴",
                    "daytemp": "18",
                    "nighttemp": "5",
                    "daywind": "南",
                    "nightwind": "南",
                    "daypower": "1-3",
                    "nightpower": "1-3",
                    "daytemp_float": "18.0",
                    "nighttemp_float": "5.0"
                },
                {
                    "date": "2026-03-24",
                    "week": "2",
                    "dayweather": "晴",
                    "nightweather": "晴",
                    "daytemp": "20",
                    "nighttemp": "7",
                    "daywind": "南",
                    "nightwind": "南",
                    "daypower": "1-3",
                    "nightpower": "1-3",
                    "daytemp_float": "20.0",
                    "nighttemp_float": "7.0"
                },
                {
                    "date": "2026-03-25",
                    "week": "3",
                    "dayweather": "晴",
                    "nightweather": "多云",
                    "daytemp": "23",
                    "nighttemp": "9",
                    "daywind": "西南",
                    "nightwind": "西南",
                    "daypower": "1-3",
                    "nightpower": "1-3",
                    "daytemp_float": "23.0",
                    "nighttemp_float": "9.0"
                }
            ]
        }

    else:
        print("未找到天气工具")

if __name__ == "__main__":
    # asyncio.run(call_amap_tools())
    asyncio.run(call_weather_tool())