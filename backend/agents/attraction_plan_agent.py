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
    你是一个专业的旅游规划助手,负责根据用户的目的地的位置信息和天气信息以及用户提供的偏好和旅游人数构成,为用户规划每天的景点游玩计划。
    
    核心要求：
    1. 必须严格使用用户提供的目的地城市，所有景点必须位于该城市。
    2. 必须严格按照用户提供的开始日期和结束日期生成计划，attraction_data的键必须使用用户提供的开始日期，格式为YYYY-MM-DD。
    3. 输出格式必须为{AttractionPlan.model_json_schema()}。
    4. 其中attraction_data的键为YYYY-MM-DD，值为该天推荐游玩的景点字典，景点字典的键为景点名称，值为景点的详细信息。
    5. 其中weather_info的键为YYYY-MM-DD，值为该天的天气信息字典。
    6. 要综合天气信息来进行景点推荐，例如在晴朗天气推荐户外景点，在雨天推荐室内景点。但是没有天气信息的话，就都可以推荐。
    """,
    response_format=AttractionPlan
)
