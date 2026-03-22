from pydantic import BaseModel, Field
from typing import List, Optional, Tuple, Dict
from typing_extensions import Annotated
from datetime import datetime

def merge_dicts(left: Dict, right: Dict) -> Dict:
    """Merge dicts, prioritizing right for conflicts."""
    return {**left, **right}

class UserPreferences(BaseModel):
    origin_city: str = Field(..., description="Starting city")
    destination_city: Optional[str] = Field(None, description="Destination city")
    travel_dates: Tuple[datetime, datetime] = Field(..., description="Travel dates")
    number_of_days: int = Field(..., description="Number of days")
    number_of_travelers: int = Field(..., description="Number of travelers")
    age_distribution: Annotated[Dict[str, int], merge_dicts]  # 成人、儿童、老人数量

    # 兴趣偏好
    interests: List[str] = Field(default_factory=list)
    accommodation_preference: str = Field(default="", description="Accommodation preference")
    special_requirements: List[str] = Field(default_factory=list, description="Special requirements")
   