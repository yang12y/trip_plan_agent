from langchain.agents import create_agent
from tools.amap_tools import AmapTools
from models.deepseek import DeepSeekModel
from struct_data.attraction_plan import AttractionPlan
import asyncio


def get_tools():
    amap_tools = AmapTools()
    tools = asyncio.run(amap_tools.get_amap_tools())
    return tools


attraction_plan_agent = create_agent(
    model=DeepSeekModel().get_attraction_plan_model(),
    tools=get_tools(),
    system_prompt=f"""
    你是一个专业的旅游规划助手,负责根据用户的目的地的天气信息和位置信息,推荐合适的景点。
    要求先获取用户的目的地的天气信息,再根据天气信息推荐合适游玩的景点。
    根据用户的旅游时间的时长,推荐合适数量的景点。
    输出格式为{AttractionPlan.model_json_schema()},其中weather_info的键为时间,值为天气信息。
    attraction_data的键为景点名称,值为景点数据。
    """,
    response_format=AttractionPlan,
)
