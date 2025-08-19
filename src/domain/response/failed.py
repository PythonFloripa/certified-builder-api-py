from pydantic import BaseModel

class FailedResponse(BaseModel):
    status: int = 500
    message: str = "Internal Server Error"
    details: str = "Internal Server Error"