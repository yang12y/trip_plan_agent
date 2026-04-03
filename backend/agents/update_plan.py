from langchain.agents import create_agent
from models.qwen import QwenModel
import asyncio

from tools.amap_tools import AmapTools
from struct_data.attraction_plan import AttractionPlan

# 延迟初始化工具，避免在模块导入时执行
update_plan_agent = None

async def get_tools():
    amap_tools = AmapTools()
    tools = await amap_tools.get_amap_tools()
    return tools

async def init_update_plan_agent():
    global update_plan_agent
    tools = await get_tools()
    update_plan_agent = create_agent(
        model=QwenModel().get_update_plan_model(),
        tools=tools,
        system_prompt=f"""
        你是一个专业的旅游规划助手,负责根据用户的目的地的位置信息和天气信息以及用户提供的偏好和旅游人数构成,规划出用户最新的旅游计划。
        要求：
        1. 根据最新的天气信息和位置信息，规划最新的旅游计划。
        2. 考虑用户的旅游人数构成,确保计划符合用户的需求。
        3. 考虑用户的住宿偏好,确保计划符合用户的需求。
        4. 考虑用户的兴趣偏好,确保计划符合用户的需求。
        5. 必须严格使用用户提供的目的地城市，所有景点必须位于该城市。
        6. 必须严格按照用户提供的开始日期和结束日期生成计划，attraction_data的键必须使用用户提供的开始日期，格式为YYYY-MM-DD。
        7. 输出格式必须为{AttractionPlan.model_json_schema()}。
        8. 其中attraction_data的键为YYYY-MM-DD，值为该天推荐游玩的景点字典，景点字典的键为景点名称，值为景点的详细信息。
        9. 其中weather_info的键为YYYY-MM-DD，值为该天的天气信息字典。
        10. 要综合天气信息来进行景点推荐，例如在晴朗天气推荐户外景点，在雨天推荐室内景点。但是没有天气信息的话，就都可以推荐。
        11. 严禁乱编景点信息以及天气信息，提供的景点信息和天气信息必须经过工具调用。
        """,
        response_format=AttractionPlan,
    )

# 提供一个同步函数来获取agent
def get_update_plan_agent():
    global update_plan_agent
    if update_plan_agent is None:
        # 在第一次调用时初始化
        import asyncio
        asyncio.run(init_update_plan_agent())
    return update_plan_agent