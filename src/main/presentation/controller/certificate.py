import logging

from src.infrastructure.aws.api_gateway_restr_resolver import app
from src.infrastructure.config.config import config
from src.main.presentation.http_types.create_certificate import CreateCertificateRequest
from aws_lambda_powertools.utilities.parser import parse
from src.main.handler.certificate import create_certificate_handler
from src.domain.response.build_order import BuildOrderResponse
from src.domain.response.failed import FailedResponse

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





