from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from src.domain.response.tech_floripa import TechOrdersResponse

class BuildOrderResponse(BaseModel):
    certificate_quantity: int
    existing_orders: List[TechOrdersResponse]
    new_orders: List[TechOrdersResponse]
    processing_date: datetime = Field(
        default_factory=datetime.now,
        description="Data de processamento da resposta"
    )