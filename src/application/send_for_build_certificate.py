import logging
from typing import List
from retry import retry
from src.infrastructure.aws.sqs_service import SQSService
from src.domain.response.tech_floripa import TechOrdersResponse


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class SendForBuildCertificate:
    """
    Classe responsável por enviar ordens para construção de certificados.
    Recebe SQSService via injeção de dependência para evitar importação circular.
    """

    def __init__(self, sqs_service: SQSService):
        """
        Inicializa a classe com o serviço SQS injetado.
        
        Args:
            sqs_service: Instância do SQSService para envio de mensagens
        """
        self.sqs_service = sqs_service


    @retry(
            exceptions=Exception,
            tries=2,
            delay=2,
            backoff=2,
            logger=logger
    )
    def execute(self, orders: List[TechOrdersResponse]):
        logger.info(f"Sending {len(orders)} orders to build certificate.")
        processed_orders = self.__processed_orders_dict(orders)
        self.__send_to_sqs(processed_orders)   


    def __processed_orders_dict(self, orders: List[TechOrdersResponse]) -> List[dict]:
        logger.info(f"Processing {len(orders)} orders to build certificate.")
        return [order.model_dump() for order in orders]
    
    def __send_to_sqs(self, orders: List[dict]):
        try:
            logger.info(f"Sending {len(orders)} orders to build certificate.")
            # self.sqs_service.send_message(orders)
            logger.info(f"Orders sent to build certificate.")
        except Exception as e:
            logger.error(f"Error sending orders to build certificate: {e}")
            raise e