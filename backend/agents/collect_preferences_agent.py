from struct_data.user_preferences import UserPreferences
from models.deepseek import DeepSeekModel

from langchain.agents import create_agent

collect_preferences_agent = create_agent(
    model=DeepSeekModel().get_collect_preferences_model(),
    tools=[],
    system_prompt=f"""从用户输入提取旅行信息以及用户兴趣偏好,按照{UserPreferences}的格式返回,如果信息不全，返回已知部分并询问缺失部分。""",
    response_format=UserPreferences
)
