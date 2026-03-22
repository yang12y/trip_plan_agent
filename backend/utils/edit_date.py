from datetime import datetime
from typing import Tuple

def adjust_end_time(travel_dates: Tuple[datetime, datetime]) -> Tuple[datetime, datetime]:
    """调整结束时间为当天的23:59:59"""
    start_date, end_date = travel_dates
    # 保持年、月、日不变，将时间设为23:59:59
    adjusted_end_date = end_date.replace(hour=23, minute=59, second=59)
    return (start_date, adjusted_end_date)