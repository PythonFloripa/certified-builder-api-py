from pydantic import BaseModel
from typing import Optional

class Response(BaseModel):
    status: int
    message: str
    details: Optional[str] = None