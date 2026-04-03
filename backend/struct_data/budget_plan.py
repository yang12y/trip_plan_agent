from pydantic import BaseModel, Field
from typing import List

class BudgetItem(BaseModel):
    category: str = Field(description="类别：交通/住宿/门票/餐饮/购物/其他")
    item_name: str = Field(description="项目名称")
    estimated_cost: float = Field(description="预估费用")
    cost_range: str = Field(description="价格区间，如：200-300")
    is_essential: bool = Field(description="是否必需")
    save_tips: str = Field(default="", description="省钱建议")

class BudgetPlan(BaseModel):
    total_cost: float = Field(description="总预估费用")
    cost_range: str = Field(description="总费用区间")
    items: List[BudgetItem] = Field(description="预算明细")
    save_tips: List[str] = Field(description="整体省钱建议")
    emergency_fund: float = Field(description="建议预留应急资金")