from data_base.storage import SQLiteStorageService
from struct_data.state import TravelPlanState


def save_node(state: TravelPlanState) -> TravelPlanState:
    """
    保存状态到 SQLite 数据库
    """
    print("开始保存状态")
    db_service = SQLiteStorageService()
    db_service.save_state(state.user_id, state)
    print("保存成功")
    return state
