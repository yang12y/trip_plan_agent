from langchain.agents import create_agent
from models.deepseek import DeepSeekModel
from struct_data.budget_plan import BudgetPlan
import asyncio

# 延迟初始化工具，避免在模块导入时执行
budget_plan_agent = None

async def init_budget_plan_agent():
    global budget_plan_agent
    budget_plan_agent = create_agent(
        model=DeepSeekModel().get_budget_plan_model(),
        tools=[],  # 可以添加查询实时票价的工具
        system_prompt=f"""
        你是一个专业的旅行预算规划师。
        
        请根据用户提供的旅行信息，生成详细的预算规划，包括：
        1. 交通费用（往返大交通 + 当地小交通）
        2. 住宿费用（根据偏好和天数计算）
        3. 门票费用（各景点门票总和）
        4. 餐饮费用（按天数和人数估算）
        5. 其他费用（购物、应急等）
        
        输出格式：{BudgetPlan.model_json_schema()}
        
        注意：
        - 费用要基于当前市场价格
        - 给出价格区间（最低-最高）
        - 标注哪些可以省钱
        """,
        response_format=BudgetPlan,
    )

# 提供一个异步函数来获取agent
async def get_budget_plan_agent():
    global budget_plan_agent
    if budget_plan_agent is None:
        # 在第一次调用时初始化
        await init_budget_plan_agent()
    return budget_plan_agent