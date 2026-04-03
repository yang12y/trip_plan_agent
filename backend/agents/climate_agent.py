import asyncio
from langchain.agents import create_agent
from tools.amap_tools import AmapTools
from models.deepseek import DeepSeekModel
from struct_data.daily_weather import DailyWeatherData

# 延迟初始化工具，避免在模块导入时执行
climate_agent = None

async def get_weather_tool():
    """
    获取天气工具
    """
    tools = await AmapTools().get_amap_tools()
    weather_tool = None
    for tool in tools:
        if tool.name == "maps_weather":
            weather_tool = tool
    return weather_tool

async def init_climate_agent():
    global climate_agent
    weather_tool = await get_weather_tool()
    climate_agent = create_agent(
        model=DeepSeekModel().get_climate_model(),
        tools=[weather_tool],
        response_format=DailyWeatherData,
        system_prompt="你是一个专业的天气助手，能够根据用户的位置和日期，提供准确的天气信息。",
    )

# 提供一个同步函数来获取agent
def get_climate_agent():
    global climate_agent
    if climate_agent is None:
        # 在第一次调用时初始化
        import asyncio
        asyncio.run(init_climate_agent())
    return climate_agent
