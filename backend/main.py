from fastapi import FastAPI
from router.trip_plan import router as trip_plan_router
from router.update_trip import router as update_trip_router
from router.get_weather import router as get_weather_router

app = FastAPI(
    title="旅行计划 API",
    description="提供旅行计划相关的 API 接口",
    version="1.0.0"
)

# 注册路由
app.include_router(trip_plan_router)
app.include_router(update_trip_router)
app.include_router(get_weather_router)


@app.get("/")
async def root():
    """
    根路径
    """
    return {"message": "欢迎使用旅行计划 API"}


@app.get("/health")
async def health_check():
    """
    健康检查
    """
    return {"status": "healthy"}
