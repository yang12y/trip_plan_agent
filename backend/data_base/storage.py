import sqlite3
import json
import os
from datetime import datetime
from struct_data.state import TravelPlanState
from langchain_core.messages import HumanMessage, AIMessage


class SQLiteStorageService:
    def __init__(self, db_path="./data_base/trip_planner.db"):
        """
        初始化 SQLite 存储服务
        :param db_path: SQLite 数据库文件路径
        """
        # 确保数据库目录存在
        db_dir = os.path.dirname(db_path)
        os.makedirs(db_dir, exist_ok=True)
        
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """
        初始化数据库，创建必要的表
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 创建用户状态表
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS travel_plan_states (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT UNIQUE NOT NULL,
                    state_data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建索引
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON travel_plan_states(user_id)')
            
            conn.commit()
    
    def save_state(self, user_id: str, state: TravelPlanState):
        """
        保存状态到 SQLite 数据库
        :param user_id: 用户 ID
        :param state: TravelPlanState 对象
        """
        # 序列化状态对象
        state_dict = state.model_dump()
        
        # 序列化消息对象
        if state_dict.get("messages"):
            serialized_messages = []
            for msg in state_dict["messages"]:
                # 检查 msg 是否已经是字典格式
                if isinstance(msg, dict):
                    # 如果是字典，直接添加
                    serialized_messages.append(msg)
                else:
                    # 如果是消息对象，序列化它
                    serialized_messages.append({
                        "type": msg.__class__.__name__,
                        "content": msg.content,
                        "additional_kwargs": msg.additional_kwargs,
                        "response_metadata": msg.response_metadata
                    })
            state_dict["messages"] = serialized_messages
        
        # 转换为 JSON 字符串
        state_json = json.dumps(state_dict, ensure_ascii=False, default=str)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 使用 UPSERT 操作：如果用户存在则更新，否则插入
            cursor.execute('''
                INSERT INTO travel_plan_states (user_id, state_data, updated_at)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    state_data = excluded.state_data,
                    updated_at = excluded.updated_at
            ''', (user_id, state_json, datetime.now().isoformat()))
            
            conn.commit()
    
    def get_state(self, user_id: str) -> TravelPlanState:
        """
        从 SQLite 数据库获取状态
        :param user_id: 用户 ID
        :return: TravelPlanState 对象，如果不存在返回 None
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # 查询用户状态
            cursor.execute('''
                SELECT state_data FROM travel_plan_states WHERE user_id = ?
            ''', (user_id,))
            
            result = cursor.fetchone()
            if not result:
                return None
            
            # 解析 JSON 数据
            state_dict = json.loads(result[0])
            
            # 反序列化消息对象
            if state_dict.get("messages"):
                deserialized_messages = []
                for msg in state_dict["messages"]:
                    # 检查 msg 是否已经是消息对象
                    if hasattr(msg, "content"):
                        # 如果是消息对象，直接添加
                        deserialized_messages.append(msg)
                    else:
                        # 如果是字典，反序列化为消息对象
                        if msg.get("type") == "HumanMessage":
                            deserialized_messages.append(HumanMessage(
                                content=msg["content"],
                                additional_kwargs=msg.get("additional_kwargs", {}),
                                response_metadata=msg.get("response_metadata", {})
                            ))
                        else:
                            deserialized_messages.append(AIMessage(
                                content=msg["content"],
                                additional_kwargs=msg.get("additional_kwargs", {}),
                                response_metadata=msg.get("response_metadata", {})
                            ))
                state_dict["messages"] = deserialized_messages
            
            # 反序列化日期时间对象
            if state_dict.get("travel_dates"):
                start_date, end_date = state_dict["travel_dates"]
                state_dict["travel_dates"] = (
                    datetime.fromisoformat(start_date),
                    datetime.fromisoformat(end_date)
                )
            
            return TravelPlanState(**state_dict)
    
    def delete_state(self, user_id: str):
        """
        删除用户状态
        :param user_id: 用户 ID
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                DELETE FROM travel_plan_states WHERE user_id = ?
            ''', (user_id,))
            
            conn.commit()
    
    def list_users(self):
        """
        列出所有用户 ID
        :return: 用户 ID 列表
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT user_id FROM travel_plan_states
            ''')
            
            return [row[0] for row in cursor.fetchall()]

if __name__ == "__main__":
    storage = SQLiteStorageService()
    state = storage.get_state("user1")
    print(state)
