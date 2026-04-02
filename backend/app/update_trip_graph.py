from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from struct_data.state import TravelPlanState
from langgraph.graph import StateGraph, START, END

from nodes.update_plan_node import update_plan_node
from nodes.get_climate_node import get_climate_node
import asyncio


def router(state: TravelPlanState) -> TravelPlanState:
    """
    路由节点
    """
    print("开始路由")
    if state.is_weather_change:
        return "update_plan_node"
    return END


graph = StateGraph(TravelPlanState)
graph.add_node("update_plan_node", update_plan_node)
graph.add_node("get_climate_node", get_climate_node)

graph.add_edge(START, "get_climate_node")
graph.add_conditional_edges(
    "get_climate_node", 
    router, 
    {"update_plan_node": "update_plan_node", END: END}
)
graph.add_edge("update_plan_node", END)

update_trip_graph = graph.compile()


