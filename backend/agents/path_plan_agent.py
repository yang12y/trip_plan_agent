from struct_data.user_preferences import UserPreferences
from struct_data.path_plan import PathPlan
from langchain.agents import create_agent
from tools.amap_tools import AmapTools
import json
import asyncio
from models.deepseek import DeepSeekModel

def get_tools():
    amap_tools = AmapTools()
    tools = asyncio.run(amap_tools.get_amap_tools())
    return tools
    

path_plan_agent = create_agent(
    model=DeepSeekModel().get_path_plan_model(),
    tools=get_tools(),
    system_prompt=f"""你是一个专业的行程规划助手，负责根据用户的需求和偏好，根据state中的distance字段（单位：公里），
    判断是否需要调用工具来计算自行车出行规划和步行出行规划，规划出自驾出行方式的行程。
    判断条件：
    1. 如果距离小于等于500公里，可以使用自行车出行规划工具。
    2. 如果距离小于等于100公里，可以使用步行出行规划工具。
    3. 必须使用驾车出行规划工具，和公交路径规划工具（公交，高铁，火车）来规划行程。
    注意：自行车出行规划工具和步行出行规划工具，只能在距离小于等于500公里和100公里时使用。
        当距离大于500公里时，只能使用驾车出行规划工具和公交路径规划工具（公交，高铁，火车）来规划行程，
        不能使用自行车出行规划工具和步行出行规划工具，输出格式中的bicycling_trip_path和walking_trip_path字段为空列表。
    输出格式为{PathPlan.model_json_schema()}。""",
    response_format=PathPlan,
)
