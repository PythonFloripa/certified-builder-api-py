import logging
from typing import Annotated, List, Optional
from aws_lambda_powertools.event_handler.openapi.params import Query
from aws_lambda_powertools.utilities.parser import parse

from aws_lambda_powertools.event_handler import Response

from src.infrastructure.aws.api_gateway_restr_resolver import app
from src.infrastructure.config.config import config

from src.main.presentation.http_types.create_certificate import CreateCertificateRequest
from src.main.presentation.http_types.fetch_certificate import FetchCertificateRequest, FetchCertificateResponse
from src.main.presentation.http_types.download_certificate import DownloadCertificateRequest, DownloadCertificateResponse
from src.main.handler.certificate import create_certificate_handler, fetch_certificate_handler, download_certificate_handler
from src.main.presentation.template_loader import template_loader
from src.domain.response.build_order import BuildOrderResponse
from src.domain.response.failed import FailedResponse
from src.domain.exception.certificate_not_found import CertificateNotFound


logger = logging.getLogger(__name__)


@app.post(f"{config.PREFIX_API_VERSION}/certificate/create")
def create_certificate() -> BuildOrderResponse: 
    try:
        request: CreateCertificateRequest = parse(app.current_event.body, CreateCertificateRequest)        
        response: BuildOrderResponse = create_certificate_handler(request)
        return response
    except Exception as e:
        logger.error(f"Erro ao processar a requisição: {e}")
        return FailedResponse(
            details=str(e),
            message="Internal Server Error",
            status=500
        )

    
@app.get(f"{config.PREFIX_API_VERSION}/certificate/fetch")
def fetch_certificate(
    order_id: Annotated[Optional[int], Query(ge=1)] = None,
    email: Annotated[Optional[str], Query(min_length=1, max_length=255)] = None,
    product_id: Annotated[Optional[int], Query(ge=1)] = None
) -> List[FetchCertificateResponse]:
    """
    Endpoint unificado para busca de certificados.
    Suporta busca por order_id, email, product_id ou combinações.
    
    Query Parameters:
    - order_id: Busca certificados por ID do pedido
    - email: Busca certificados por email do participante
    - product_id: Busca certificados por ID do produto
    - email + product_id: Busca específica por email e produto
    """
    try:
        request: FetchCertificateRequest = FetchCertificateRequest(
            order_id=order_id,
            email=email,
            product_id=product_id
        )
        response: List[FetchCertificateResponse] = fetch_certificate_handler(request)
        return response
    except Exception as e:
        if isinstance(e, CertificateNotFound):
            return FailedResponse(
                details=str(e),
                message=e.message,
                status=404
            )
        else:
            logger.error(f"Erro ao processar a requisição: {e}")
            return FailedResponse(
                details=str(e),
                message="Internal Server Error",
                status=500
            )
        


@app.get(f"{config.PREFIX_API_VERSION}/certificate/download")
def download_certificate(
    id: Annotated[str, Query(description="UUID do certificado")]
):
    try:
        import uuid
        certificate_id = uuid.UUID(id)
        
        response = download_certificate_handler(
            DownloadCertificateRequest(id=certificate_id)
        )
        
        if response.success:
            html_content = template_loader.load_template(
                "certificate_download.html",
                certificate_url=response.certificate_url
            )
            return Response(
                status_code=200,
                content_type="text/html",
                body=html_content
            )
        else:
            html_content = template_loader.load_template("certificate_not_generated.html")
            return Response(
                status_code=200,
                content_type="text/html",
                body=html_content
            )
        
    except ValueError:
        html_content = template_loader.load_template("certificate_uuid_invalid.html")
        return Response(
            status_code=404,
            content_type="text/html",
            body=html_content
        )
    except CertificateNotFound:
        html_content = template_loader.load_template("certificate_not_found.html")
        return Response(
            status_code=404,
            content_type="text/html",
            body=html_content
        )
    except Exception as e:
        logger.error(f"Erro ao processar a requisição: {e}")
        html_content = template_loader.load_template("server_error.html")
        return Response(
            status_code=500,
            content_type="text/html",
            body=html_content
        )
