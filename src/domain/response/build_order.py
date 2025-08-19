from pydantic import BaseModel, Field
from typing import List, Any
from datetime import datetime

class BuildOrderResponse(BaseModel):
    certificate_quantity: int
    existing_orders: List[Any]
    new_orders: List[Any]
    processing_date: datetime = Field(default_factory=datetime.now)