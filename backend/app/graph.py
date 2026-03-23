from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from struct_data.state import TravelPlanState
from langgraph.graph import StateGraph, START, END
from nodes.collection_preferences_node import collect_preferences_node
from nodes.path_plan_node import path_plan_node
from nodes.caculate_distance_node import caculate_distance_node
from nodes.attraction_plan_node import attraction_plan_node
import asyncio

# 初始化图
graph = StateGraph(TravelPlanState)
graph.add_node("preferences", collect_preferences_node)
graph.add_node("path_plan", path_plan_node)
graph.add_node("caculate_distance", caculate_distance_node)
graph.add_node("attraction_plan", attraction_plan_node)
graph.add_edge(START, "preferences")
graph.add_edge("preferences", "caculate_distance")
graph.add_edge("caculate_distance", "path_plan")
graph.add_edge("path_plan", "attraction_plan")
graph.add_edge("attraction_plan", END)
app = graph.compile()

# 初始化状态
initial_state = TravelPlanState(
    user_id="user1",
    messages=[HumanMessage(content="从南昌去上海，1月1-3日，2成人1小孩，喜欢文化、自然、美食，在酒店住宿，最好做高铁")]
)

updated_state = asyncio.run(app.ainvoke(initial_state))

print(updated_state['attraction_data'])