import json
import logging
from typing import List, Optional
from src.domain.entity.certificate import Certificate
from src.domain.repository.certificate_repository import CertificateRepository
from src.infrastructure.aws.dynamodb_service import DynamoDBService

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class CertificateRepositoryImpl(CertificateRepository):
    """
    Implementação concreta do repositório de Certificate usando DynamoDB.
    Segue Clean Architecture implementando a interface do domínio.
    """
    
    def __init__(self, dynamodb_service: DynamoDBService, table_name: str = "certificates"):
        self.dynamodb_service = dynamodb_service
        self.table_name = table_name
    
    async def create(self, entity: Certificate) -> Certificate:
        """
        Cria um novo certificado no DynamoDB.
        
        Args:
            entity: Certificado a ser criado
            
        Returns:
            Certificate: Certificado criado
        """
        try:
            # Converte a entidade para dicionário
            item = entity.model_dump()
            
            # Adiciona o item no DynamoDB
            self.dynamodb_service.put_item(item, self.table_name)
            
            logger.info(f"Certificado criado com sucesso: {entity.id}")
            return entity
            
        except Exception as e:
            logger.error(f"Erro ao criar certificado: {str(e)}")
            raise
    
    async def get_by_id(self, entity_id: str) -> Optional[Certificate]:
        """
        Busca um certificado pelo ID.
        
        Args:
            entity_id: ID do certificado
            
        Returns:
            Optional[Certificate]: Certificado encontrado ou None
        """
        try:
            key = {"id": entity_id}
            item = self.dynamodb_service.get_item(key, self.table_name)
            
            if item:
                return Certificate(**item)
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar certificado por ID {entity_id}: {str(e)}")
            raise
    
    async def get_all(self) -> List[Certificate]:
        """
        Busca todos os certificados.
        
        Returns:
            List[Certificate]: Lista de todos os certificados
        """
        try:
            items = self.dynamodb_service.scan_table(self.table_name)
            certificates = []
            
            for item in items:
                certificates.append(Certificate(**item))
            
            return certificates
            
        except Exception as e:
            logger.error(f"Erro ao buscar todos os certificados: {str(e)}")
            raise
    
    async def update(self, entity_id: str, entity: Certificate) -> Optional[Certificate]:
        """
        Atualiza um certificado existente.
        
        Args:
            entity_id: ID do certificado
            entity: Novos dados do certificado
            
        Returns:
            Optional[Certificate]: Certificado atualizado ou None se não encontrado
        """
        try:
            # Verifica se o certificado existe
            if not await self.exists(entity_id):
                return None
            
            # Converte a entidade para dicionário
            update_data = entity.model_dump()
            
            # Remove o ID do update_data para não atualizar a chave primária
            if 'id' in update_data:
                del update_data['id']
            
            # Constrói a expressão de atualização
            update_expression = "SET "
            expression_values = {}
            
            for key, value in update_data.items():
                if value is not None:
                    update_expression += f"#{key} = :{key}, "
                    expression_values[f":{key}"] = value
            
            # Remove a vírgula extra no final
            update_expression = update_expression.rstrip(", ")
            
            # Adiciona os nomes dos atributos
            expression_names = {f"#{key}": key for key in update_data.keys() if update_data[key] is not None}
            
            # Atualiza o item
            key = {"id": entity_id}
            response = self.dynamodb_service.aws.update_item(
                TableName=self.table_name,
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ExpressionAttributeNames=expression_names,
                ReturnValues="ALL_NEW"
            )
            
            if 'Attributes' in response:
                return Certificate(**response['Attributes'])
            return None
            
        except Exception as e:
            logger.error(f"Erro ao atualizar certificado {entity_id}: {str(e)}")
            raise
    
    async def delete(self, entity_id: str) -> bool:
        """
        Remove um certificado.
        
        Args:
            entity_id: ID do certificado
            
        Returns:
            bool: True se removido com sucesso, False caso contrário
        """
        try:
            key = {"id": entity_id}
            self.dynamodb_service.delete_item(key, self.table_name)
            
            logger.info(f"Certificado {entity_id} removido com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao remover certificado {entity_id}: {str(e)}")
            return False
    
    async def exists(self, entity_id: str) -> bool:
        """
        Verifica se um certificado existe.
        
        Args:
            entity_id: ID do certificado
            
        Returns:
            bool: True se existe, False caso contrário
        """
        try:
            key = {"id": entity_id}
            item = self.dynamodb_service.get_item(key, self.table_name)
            return item is not None
            
        except Exception as e:
            logger.error(f"Erro ao verificar existência do certificado {entity_id}: {str(e)}")
            return False
    
    async def get_by_order_id(self, order_id: int) -> List[Certificate]:
        """
        Busca certificados por order_id.
        
        Args:
            order_id: ID do pedido
            
        Returns:
            List[Certificate]: Lista de certificados do pedido
        """
        try:
            filter_expression = "order_id = :order_id"
            expression_values = {":order_id": order_id}
            
            items = self.dynamodb_service.scan_table(
                self.table_name, 
                filter_expression, 
                expression_values
            )
            
            certificates = []
            for item in items:
                certificates.append(Certificate(**item))
            
            return certificates
            
        except Exception as e:
            logger.error(f"Erro ao buscar certificados por order_id {order_id}: {str(e)}")
            raise
    
    async def get_by_participant_email(self, email: str) -> List[Certificate]:
        """
        Busca certificados por email do participante.
        
        Args:
            email: Email do participante
            
        Returns:
            List[Certificate]: Lista de certificados do participante
        """
        try:
            filter_expression = "participant_email = :email"
            expression_values = {":email": email}
            
            items = self.dynamodb_service.scan_table(
                self.table_name, 
                filter_expression, 
                expression_values
            )
            
            certificates = []
            for item in items:
                certificates.append(Certificate(**item))
            
            return certificates
            
        except Exception as e:
            logger.error(f"Erro ao buscar certificados por email {email}: {str(e)}")
            raise
    
    async def get_by_product_id(self, product_id: int) -> List[Certificate]:
        """
        Busca certificados por product_id.
        
        Args:
            product_id: ID do produto
            
        Returns:
            List[Certificate]: Lista de certificados do produto
        """
        try:
            filter_expression = "product_id = :product_id"
            expression_values = {":product_id": product_id}
            
            items = self.dynamodb_service.scan_table(
                self.table_name, 
                filter_expression, 
                expression_values
            )
            
            certificates = []
            for item in items:
                certificates.append(Certificate(**item))
            
            return certificates
            
        except Exception as e:
            logger.error(f"Erro ao buscar certificados por product_id {product_id}: {str(e)}")
            raise
    
    async def get_successful_certificates(self) -> List[Certificate]:
        """
        Busca apenas certificados com sucesso=True.
        
        Returns:
            List[Certificate]: Lista de certificados bem-sucedidos
        """
        try:
            filter_expression = "success = :success"
            expression_values = {":success": True}
            
            items = self.dynamodb_service.scan_table(
                self.table_name, 
                filter_expression, 
                expression_values
            )
            
            certificates = []
            for item in items:
                certificates.append(Certificate(**item))
            
            return certificates
            
        except Exception as e:
            logger.error(f"Erro ao buscar certificados bem-sucedidos: {str(e)}")
            raise
