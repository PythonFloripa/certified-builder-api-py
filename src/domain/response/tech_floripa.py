from pydantic import BaseModel, Field
from typing import Optional

class TechOrdersResponse(BaseModel):
    order_id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    cpf: str
    city: str
    product_id: int
    product_name: str
    certificate_details: str
    certificate_logo: str
    certificate_background: str
    order_date: str
    checkin_latitude: Optional[str]
    checkin_longitude: Optional[str]
    time_checkin: Optional[str]


    # method to check if time_checkin is not None
    def is_empty_time_checkin(self) -> bool:
        return self.time_checkin is None or self.time_checkin == ""