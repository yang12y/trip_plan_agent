from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()


qwen_model = OpenAI(
    api_key=os.getenv("QWEN_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


class QwenModel:
    def __init__(self):
        self.model = qwen_model
        
    def get_path_plan_model(self):
        """
        获取PathPlan模型
        """
        return self.model