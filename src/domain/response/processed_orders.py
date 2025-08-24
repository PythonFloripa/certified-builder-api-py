from pydantic import BaseModel, Field
from typing import List
from src.domain.response.tech_floripa import TechOrdersResponse



class ProcessedOrdersResponse(BaseModel):
    valid_orders: List[TechOrdersResponse]
    invalid_orders: List[TechOrdersResponse]