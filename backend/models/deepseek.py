from langchain_deepseek import ChatDeepSeek

from config import Config

class DeepSeekModel:
    def __init__(self):
        self.collect_preferences_model = ChatDeepSeek(
            api_key=Config.DEEPSEEK_API_KEY_1,
            model="deepseek-chat",
        )

        self.path_plan_model = ChatDeepSeek(
            api_key=Config.DEEPSEEK_API_KEY_2,
            model="deepseek-chat",
            max_tokens = 8192
        )
        
        self.attraction_plan_model = ChatDeepSeek(
            api_key=Config.DEEPSEEK_API_KEY_1,
            model="deepseek-chat",
        )

    def get_collect_preferences_model(self):
        """
        获取CollectPreferences模型
        """
        return self.collect_preferences_model
        
    def get_path_plan_model(self):
        """
        获取PathPlan模型
        """
        return self.path_plan_model
        
    def get_attraction_plan_model(self):
        """
        获取AttractionPlan模型
        """
        return self.attraction_plan_model