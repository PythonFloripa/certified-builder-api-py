from pydantic import BaseModel, Field
from typing import Optional
import uuid

class Certificate(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    success: Optional[bool] = False
    certificate_key: Optional[str] = None
    certificate_url: Optional[str] = None
    generated_date: Optional[str] = None
    order_id: Optional[int]
    order_date: Optional[str]
    product_id: Optional[int]
    product_name: Optional[str]
    certificate_details: Optional[str]
    certificate_logo: Optional[str]
    certificate_background: Optional[str]
    participant_email: Optional[str]
    participant_first_name: Optional[str]
    participant_last_name: Optional[str]
    participant_cpf: Optional[str]
    participant_phone: Optional[str]
    participant_city: Optional[str]
