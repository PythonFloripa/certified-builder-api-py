from pydantic import BaseModel, Field

class FailedResponse(BaseModel):
    status: int = Field(default=500, description="Status da resposta")
    message: str = Field(default="Internal Server Error", description="Mensagem de erro")
    details: str = Field(default="Internal Server Error", description="Detalhes do erro")