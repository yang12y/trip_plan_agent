from langchain_openai import ChatOpenAI
import os
from dotenv import load_dotenv
load_dotenv()


qwen_model = ChatOpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen2.5-72b-instruct"
)


class QwenModel:
    def __init__(self):
        self.model = qwen_model
        
    def get_update_plan_model(self):
        """
        获取UpdatePlan模型
        """
        return self.model