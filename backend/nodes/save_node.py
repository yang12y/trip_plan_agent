from data_base.storage import SQLiteStorageService
from struct_data.state import TravelPlanState
import asyncio


async def save_node(state: TravelPlanState) -> TravelPlanState:
    """
    保存状态到 SQLite 数据库
    """
    print("开始保存状态")
    # 使用 asyncio.to_thread 来执行同步的数据库操作，避免阻塞事件循环
    db_service = SQLiteStorageService()
    await asyncio.to_thread(db_service.save_state, state.user_id, state)
    print("保存成功")
    return state
