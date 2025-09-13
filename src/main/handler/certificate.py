import logging
from typing import List
from src.main.presentation.http_types.create_certificate import CreateCertificateRequest
from src.main.presentation.http_types.fetch_certificate import FetchCertificateRequest, FetchCertificateResponse
from src.main.presentation.http_types.download_certificate import DownloadCertificateRequest, DownloadCertificateResponse
from src.application.dto.fetch_certificate_dto import FetchCertificateRequestDto
from src.domain.response.build_order import BuildOrderResponse
from src.domain.response.tech_floripa import TechOrdersResponse
from src.domain.response.processed_orders import ProcessedOrdersResponse
from src.application.create_certificate import CreateCertificate
from src.application.send_for_build_certificate import SendForBuildCertificate
from src.application.fetch_order_tech_floripa import FetchOrderTechFloripa
from src.application.fetch_certificate import FetchCertificate
from src.application.download_certificate import DownloadCertificate
from src.infrastructure.container.dependency_container import container


logger = logging.getLogger(__name__)


def create_certificate_handler(request: CreateCertificateRequest) -> BuildOrderResponse:
    logger.info(f"Iniciando processamento de certificados para o product_id: {request.product_id}")

    create_certificate: CreateCertificate = container.get('create_certificate')
    send_for_build_certificate: SendForBuildCertificate = container.get('send_for_build_certificate')
        
    fetch_order_tech_floripa: FetchOrderTechFloripa = container.get('fetch_order_tech_floripa')

    # Busca as ordens da API externa
    logger.info(f"Buscando ordens para product_id: {request.product_id}")
    orders_data = fetch_order_tech_floripa.fetch_orders(request.product_id)
        
    # Converte os dados para o modelo esperado
    tech_orders: List[TechOrdersResponse] = [
            TechOrdersResponse.model_validate(order_data) 
            for order_data in orders_data
        ]

    processed_orders: ProcessedOrdersResponse = create_certificate.execute(tech_orders)

        
    if len(processed_orders.valid_orders) > 0:
        logger.info(f"Enviando {len(processed_orders.valid_orders)} novas ordens para construção de certificados")
        send_for_build_certificate.execute(processed_orders.valid_orders)
    else:
        logger.info("Nenhuma ordem nova para enviar para construção de certificados")
   
    
    return BuildOrderResponse(
        certificate_quantity=len(tech_orders),
        existing_orders=[order.order_id for order in processed_orders.invalid_orders],
        new_orders=[order.order_id for order in processed_orders.valid_orders]
    )


def fetch_certificate_handler(request: FetchCertificateRequest) -> List[FetchCertificateResponse]:
    logger.info(f"Fetching certificate for request: {request}")
    
    # Converte DTO da Presentation para DTO da Application
    application_request = FetchCertificateRequestDto(
        order_id=request.order_id,
        email=request.email,
        product_id=request.product_id
    )
    
    # Executa na camada de aplicação
    fetch_certificate: FetchCertificate = container.get('fetch_certificate')
    application_responses = fetch_certificate.execute(application_request)
    
    # Converte DTOs da Application para DTOs da Presentation
    presentation_responses = []
    for app_response in application_responses:
        presentation_response = FetchCertificateResponse(
            id=app_response.id,
            order_id=app_response.order_id,
            product_id=app_response.product_id,
            participant_name=app_response.participant_name,
            participant_email=app_response.participant_email,
            participant_document=app_response.participant_document,
            certificate_url=app_response.certificate_url,
            created_at=app_response.created_at,
            updated_at=app_response.updated_at,
            success=app_response.success,
            email=app_response.email
        )
        presentation_responses.append(presentation_response)
    
    return presentation_responses


def download_certificate_handler(request: DownloadCertificateRequest) -> DownloadCertificateResponse:
    logger.info(f"Downloading certificate for request: {request}")
    
    from src.application.dto.download_certificate_dto import DownloadCertificateRequestDto
    
    application_request = DownloadCertificateRequestDto(id=request.id)
    
    download_certificate: DownloadCertificate = container.get('download_certificate')
    application_response = download_certificate.execute(application_request)
    
    response = DownloadCertificateResponse(
        certificate_url=application_response.certificate_url,
        email=application_response.email,
        product_id=application_response.product_id,
        success=application_response.success
    )

    return response
