import json
import logging
import uuid
from botocore.exceptions import ClientError
from typing import Dict, List

from src.infrastructure.aws.boto_aws import get_instance_aws, ServiceNameAWS
from src.infrastructure.config.config import config

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class SQSService:
    def __init__(self):
        self.aws = get_instance_aws(ServiceNameAWS.SQS)
        self.queue_url = config.QUEUE_URL        

    def send_message(self, messagens: List[Dict]):
        try:
            # Add MessageGroupId for FIFO queue
            # Using order_id as MessageGroupId to ensure messages for the same order are processed in order
            message_group_id = str(uuid.uuid4())
            message_deduplication_id = str(uuid.uuid4())
            logger.info(f"Enviando mensagem para a fila {self.queue_url} com MessageGroupId: {message_group_id} e MessageDeduplicationId: {message_deduplication_id}, com {len(messagens)} mensagens")
            response = self.aws.send_message(
                QueueUrl=self.queue_url,
                MessageBody=json.dumps(messagens),
                MessageGroupId=message_group_id,
                MessageDeduplicationId=message_deduplication_id,
            )
            logger.info(f"Mensagem enviada com sucesso: {response['MessageId']}")
            return response
        except ClientError as e:
            logger.error(f"Erro ao enviar mensagem para a fila {self.queue_url}: {str(e)}")
            raise