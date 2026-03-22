import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from config import Config

# 获取高德地图工具
class AmapTools:
    def __init__(self):
        self.config = Config()
        self.tools = None
        self.client = MultiServerMCPClient({
            "amap-maps": {
                "transport": "streamable_http",
                "url": self.config.AMAP_URI,
            }
        })
    
    async def get_amap_tools(self):
        """
        获取高德地图工具列表
        """
        if self.tools is None:
            self.tools = await self.client.get_tools()
        return self.tools

async def main():
    amap_tools = AmapTools()
    tools = await amap_tools.get_amap_tools()
    # print(type(tools))
    for tool in tools:
        print(tool)
    print(type(tools[0]))
    return tools

if __name__ == "__main__":
    tools = asyncio.run(main())
    """
name='maps_regeocode' description='将一个高德经纬度坐标转换为行政区划地址信息' args_schema={'type': 'object', 'properties': {'location': {'type': 'string', 'description': '经纬度'}}, 'required': ['location']} response_format='content_and_artifact' coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x000002EA580BFE20>
name='maps_geo' description='将详细的结构化地址转换为经纬度坐标。支持对地标性名胜景区、建筑物名称解析为经纬度坐标' args_schema={'type': 'object', 'properties': {'address': {'type': 'string', 'description': '待解析的结构化 地址信息'}, 'city': {'type': 'string', 'description': '指定查询的城市'}}, 'required': ['address']} response_format='content_and_artifact' coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x000002EA584513A0>
name='maps_ip_location' description='IP 定位根据用户输入的 IP 地址，定位 IP 的所在位置' args_schema={'type': 'object', 'properties': {'ip': {'type': 'string', 'description': 'IP地址'}}, 'required': ['ip']} response_format='content_and_artifact' coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x000002EA584BAE80>
name='maps_weather' description='根据城市名称或者标准adcode查询指定城市的天气' args_schema={'type': 'object', 'properties': {'city': {'type': 'string', 'description': '城市名称或者adcode'}}, 'required': ['city']} response_format='content_and_artifact' coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x000002EA584BACA0>
name='maps_search_detail' description='查询关键词搜或者周边搜获取到的POI ID的详细信息' args_schema={'type': 'object', 'properties': {'id': {'type': 'string', 'description': '关键词搜或者周边搜获取到的POI ID'}}, 'required': ['id']} response_format='content_and_artifact' coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x000002EA584BB920>
name='maps_bicycling' description='骑行路径规划用于规划骑行通勤方案，规划时会考虑天桥、单行线、封路等情况。最大支持 500km 的骑行路线规划' args_schema={'type': 'object', 'properties': {'origin': {'type': 'string', 'description': '出发点经纬度，坐标格式为：经度，纬度'}, 'destination': {'type': 'string', 'description': '目的地经纬度，坐标格式为：经度，纬度'}}, 'required': ['origin', 'destination']} response_format='content_and_artifact' coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x000002EA584BB9C0>
name='maps_direction_walking' description='步行路径规划 API 可以根据输入起点终点经纬度坐标规划100km 以内的步行 通勤方案，并且返回通勤方案的数据' args_schema={'type': 'object', 'properties': {'origin': {'type': 'string', 'description': '出发点经度，纬度，坐标格式为：经度，纬度'}, 'destination': {'type': 'string', 'description': '目 的地经度，纬度，坐标格式为：经度，纬度'}}, 'required': ['origin', 'destination']} response_format='content_and_artifact' coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x000002EA584BB060>     
name='maps_direction_driving' description='驾车路径规划 API 可以根据用户起终点经纬度坐标规划以小客车、轿车通勤 出行的方案，并且返回通勤方案的数据。' args_schema={'type': 'object', 'properties': {'origin': {'type': 'string', 'description': '出发点经度，纬度，坐标格式为：经度，纬度'}, 'destination': {'type': 'string', 'description': '目的地经度，纬度，坐标格式为：经度，纬度'}}, 'required': ['origin', 'destination']} response_format='content_and_artifact' coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x000002EA584BB4C0>  
name='maps_direction_transit_integrated' description='公交路径规划 API 可以根据用户起终点经纬度坐标规划综合各类公共（火车、公交、地铁）交通方式的通勤方案，并且返回通勤方案的数据，跨城场景下必须传起点城市与终点城市' args_schema={'type': 'object', 'properties': {'origin': {'type': 'string', 'description': '出发点经度，纬度，坐标格式 为：经度，纬度'}, 'destination': {'type': 'string', 'description': '目的地经度，纬度，坐标格式为：经度，纬度'}, 'city': {'type': 'string', 'description': '公共交通规划起点城市'}, 'cityd': {'type': 'string', 'description': '公共交通规划终点城市'}}, 'required': ['origin', 'destination', 'city', 'cityd']} response_format='content_and_artifact' coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x000002EA584BBBA0>     
name='maps_distance' description='距离测量 API 可以测量两个经纬度坐标之间的距离,支持驾车、步行以及球面距离测量' args_schema={'type': 'object', 'properties': {'origins': {'type': 'string', 'description': '起点经度，纬度，可以传多个坐标，使用竖线隔离，比如120,30|120,31，坐标格式为：经度，纬度'}, 'destination': {'type': 'string', 'description': '终点经度，纬度，坐标格式为：经度，纬度'}, 'type': {'type': 'string', 'description': '距离测量类型,1代表驾车距离测量，0代表直线距离测量，3步行距离测量'}}, 'required': ['origins', 'destination']} response_format='content_and_artifact' coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x000002EA584BB880>
name='maps_text_search' description='关键词搜，根据用户传入关键词，搜索出相关的POI' args_schema={'type': 'object', 'properties': {'keywords': {'type': 'string', 'description': '搜索关键词'}, 'city': {'type': 'string', 'description': '查询城市'}, 'types': {'type': 'string', 'description': 'POI类型，比如加油站'}}, 'required': ['keywords']} response_format='content_and_artifact' coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x000002EA584BAFC0>
name='maps_around_search' description='周边搜，根据用户传入关键词以及坐标location，搜索出radius半径范围的POI' args_schema={'type': 'object', 'properties': {'keywords': {'type': 'string', 'description': '搜索关键词'}, 'location': {'type': 'string', 'description': '中心点经度纬度'}, 'radius': {'type': 'string', 'description': '搜索半径'}}, 'required': ['location']} response_format='content_and_artifact' coroutine=<function convert_mcp_tool_to_langchain_tool.<locals>.call_tool at 0x000002EA584BB6A0>
<class 'langchain_core.tools.structured.StructuredTool'>
    """