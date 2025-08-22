import json
import logging
from typing import List, Optional
from src.domain.entity.certificate import Certificate
from src.domain.repository.certificate_repository import CertificateRepository
from src.infrastructure.aws.dynamodb_service import DynamoDBService

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class CertificateRepositoryImpl(CertificateRepository):    
    def __init__(self, dynamodb_service: DynamoDBService, table_name: str = "certificates"):
        self.dynamodb_service = dynamodb_service
        self.table_name = table_name
    
    def create(self, entity: Certificate) -> Certificate:
        
        try:
            item = entity.model_dump()
            self.dynamodb_service.put_item(item, self.table_name)
            
            logger.info(f"Certificado criado com sucesso: {entity.id}")
            return entity
            
        except Exception as e:
            logger.error(f"Erro ao criar certificado: {str(e)}")
            raise
    
    def get_by_id(self, entity_id: str, order_id: int = None) -> Optional[Certificate]:
        
        try:
            # Como a tabela tem chave composta (id + order_id), precisamos de ambos
            if order_id is None:
                # Se não fornecer order_id, usa scan para buscar apenas por id
                filter_expression = "id = :id"
                expression_values = {":id": entity_id}
                
                items = self.dynamodb_service.scan_table(
                    self.table_name, 
                    filter_expression, 
                    expression_values
                )
                
                if items:
                    return Certificate(**items[0])
                return None
            else:
                # Se fornecer order_id, usa get_item com chave composta
                key = {"id": entity_id, "order_id": order_id}
                item = self.dynamodb_service.get_item(key, self.table_name)
                
                if item:
                    return Certificate(**item)
                return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar certificado por ID {entity_id}: {str(e)}")
            raise
    
    def get_all(self) -> List[Certificate]:
        
        try:
            items = self.dynamodb_service.scan_table(self.table_name)
            certificates = []
            
            for item in items:
                certificates.append(Certificate(**item))
            
            return certificates
            
        except Exception as e:
            logger.error(f"Erro ao buscar todos os certificados: {str(e)}")
            raise
    
    def update(self, entity_id: str, entity: Certificate) -> Optional[Certificate]:
        
        try:
            # Verifica se o certificado existe
            if not self.exists(entity_id):
                return None
            
            # Converte a entidade para dicionário
            update_data = entity.model_dump()
            
            # Remove o ID do update_data para não atualizar a chave primária
            if 'id' in update_data:
                del update_data['id']
            
            # Constrói a expressão de atualização
            update_expression = "SET "
            expression_values = {}
            expression_names = {}
            
            for key, value in update_data.items():
                if value is not None:
                    update_expression += f"#{key} = :{key}, "
                    expression_values[f":{key}"] = value
                    expression_names[f"#{key}"] = key
            
            # Remove a vírgula extra no final
            update_expression = update_expression.rstrip(", ")
            
            # Converte os valores para o formato JSON do DynamoDB
            expression_values = self.dynamodb_service._convert_to_dynamodb_format(expression_values)
            
            # Atualiza o item
            key = {"id": entity_id}
            # Converte a chave para o formato JSON do DynamoDB
            key = self.dynamodb_service._convert_to_dynamodb_format(key)
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
    
    def delete(self, entity_id: str, order_id: int = None) -> bool:
        
        try:
            # Como a tabela tem chave composta (id + order_id), precisamos de ambos
            if order_id is None:
                # Se não fornecer order_id, usa scan para buscar e depois deletar
                filter_expression = "id = :id"
                expression_values = {":id": entity_id}
                
                items = self.dynamodb_service.scan_table(
                    self.table_name, 
                    filter_expression, 
                    expression_values
                )
                
                if items:
                    # Deleta o primeiro item encontrado
                    item = items[0]
                    key = {"id": item['id'], "order_id": item['order_id']}
                    self.dynamodb_service.delete_item(key, self.table_name)
                    
                    logger.info(f"Certificado {entity_id} removido com sucesso")
                    return True
                return False
            else:
                # Se fornecer order_id, usa delete_item com chave composta
                key = {"id": entity_id, "order_id": order_id}
                self.dynamodb_service.delete_item(key, self.table_name)
                
                logger.info(f"Certificado {entity_id} removido com sucesso")
                return True
            
        except Exception as e:
            logger.error(f"Erro ao remover certificado {entity_id}: {str(e)}")
            return False
    
    def exists(self, entity_id: str, order_id: int = None) -> bool:
        try:
            # Como a tabela tem chave composta (id + order_id), precisamos de ambos
            if order_id is None:
                # Se não fornecer order_id, usa scan para buscar apenas por id
                filter_expression = "id = :id"
                expression_values = {":id": entity_id}
                
                items = self.dynamodb_service.scan_table(
                    self.table_name, 
                    filter_expression, 
                    expression_values
                )
                
                return len(items) > 0
            else:
                # Se fornecer order_id, usa get_item com chave composta
                key = {"id": entity_id, "order_id": order_id}
                item = self.dynamodb_service.get_item(key, self.table_name)
                return item is not None
            
        except Exception as e:
            logger.error(f"Erro ao verificar existência do certificado {entity_id}: {str(e)}")
            return False
    
    def get_by_order_id(self, order_id: int) -> List[Certificate]:
        
        try:
            # Como a tabela tem chave composta (id + order_id), usamos scan para buscar por order_id
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
    
    def get_by_participant_email(self, email: str) -> List[Certificate]:
        
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
    
    def get_by_product_id(self, product_id: int) -> List[Certificate]:
        
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
    
    def get_successful_certificates(self) -> List[Certificate]:
        
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
