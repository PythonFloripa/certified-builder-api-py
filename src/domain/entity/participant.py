from pydantic import BaseModel, Field
import uuid
from typing import Optional

class Participant(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    first_name: str
    last_name: str
    email: str
    phone: Optional[str] = None
    cpf: Optional[str] = None
    city: Optional[str] = None