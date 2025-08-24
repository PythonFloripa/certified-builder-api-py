import logging
from typing import List
from src.main.presentation.http_types.create_certificate import CreateCertificateRequest
from src.domain.response.build_order import BuildOrderResponse
from src.domain.response.tech_floripa import TechOrdersResponse
from src.domain.response.processed_orders import ProcessedOrdersResponse
from src.application.create_certificate import CreateCertificate
from src.application.send_for_build_certificate import SendForBuildCertificate
from src.application.fetch_order_tech_floripa import FetchOrderTechFloripa
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


    