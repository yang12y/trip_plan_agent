import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    DEEPSEEK_API_KEY_1 = os.getenv("DEEPSEEK_API_KEY_1")
    DEEPSEEK_API_KEY_2 = os.getenv("DEEPSEEK_API_KEY_2")
    QWEN_API_KEY = os.getenv("QWEN_API_KEY")
    AMAP_URI = os.getenv("AMAP_URI")
    WEATHER_URI = os.getenv("WEATHER_URI")