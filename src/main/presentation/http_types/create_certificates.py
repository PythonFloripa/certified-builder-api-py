from pydantic import BaseModel
from typing import List, Optional


class CertificateItemRequest(BaseModel):
    """Modelo para um item individual de certificado na lista"""
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
    checkin_latitude: Optional[str] = None
    checkin_longitude: Optional[str] = None
    time_checkin: Optional[str] = None


class CreateCertificatesRequest(BaseModel):
    """Request para criação de múltiplos certificados"""
    certificates: List[CertificateItemRequest]

