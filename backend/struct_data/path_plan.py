from pydantic import BaseModel, Field
from typing import List, Optional, Tuple, Dict
from typing_extensions import Annotated
from operator import add
from struct_data.state import LocationInfo

class PathPlan(BaseModel):
    driving_trip_path: Annotated[List[dict], add] = Field(
        default_factory=list, 
        description="起始地到目的地的驾车行程路径"
    )
    bicycling_trip_path: Annotated[List[dict], add] = Field(
        default_factory=list, 
        description="起始地到目的地的骑行行程路径,distance小于等于500公里才进行骑行行程路径规划"
    )
    walking_trip_path: Annotated[List[dict], add] = Field(
        default_factory=list, 
        description="起始地到目的地的步行行程路径,distance小于等于100公里才进行步行行程路径规划"
    )
    transit_integrated_trip_path: Annotated[List[dict], add] = Field(
        default_factory=list, 
        description="起始地到目的地的公交路径规划行程路径"
    )
