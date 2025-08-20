import json
import logging
from typing import List, Optional
from src.domain.entity.participant import Participant
from src.domain.repository.participant_repository import ParticipantRepository
from src.infrastructure.aws.dynamodb_service import DynamoDBService

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class ParticipantRepositoryImpl(ParticipantRepository):    
    def __init__(self, dynamodb_service: DynamoDBService, table_name: str = "participants"):
        self.dynamodb_service = dynamodb_service
        self.table_name = table_name
    
    async def create(self, entity: Participant) -> Participant:        
        try:
            item = entity.model_dump()
            self.dynamodb_service.put_item(item, self.table_name)
            return entity
        except Exception as e:
            logger.error(f"Erro ao criar participante: {str(e)}")
            raise
    
    async def get_by_id(self, entity_id: str) -> Optional[Participant]:        
        try:
            key = {"id": entity_id}
            item = self.dynamodb_service.get_item(key, self.table_name)
            
            if item:
                return Participant(**item)
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar participante por ID {entity_id}: {str(e)}")
            raise
    
    async def get_all(self) -> List[Participant]:        
        try:
            items = self.dynamodb_service.scan_table(self.table_name)
            participants = []
            
            for item in items:
                participants.append(Participant(**item))
            
            return participants
            
        except Exception as e:
            logger.error(f"Erro ao buscar todos os participantes: {str(e)}")
            raise
    
    async def update(self, entity_id: str, entity: Participant) -> Optional[Participant]:        
        try:
            # Verifica se o participante existe
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
                return Participant(**response['Attributes'])
            return None
            
        except Exception as e:
            logger.error(f"Erro ao atualizar participante {entity_id}: {str(e)}")
            raise
    
    async def delete(self, entity_id: str) -> bool:        
        try:
            key = {"id": entity_id}
            self.dynamodb_service.delete_item(key, self.table_name)            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao remover participante {entity_id}: {str(e)}")
            return False
    
    async def exists(self, entity_id: str) -> bool:        
        try:
            key = {"id": entity_id}
            item = self.dynamodb_service.get_item(key, self.table_name)
            return item is not None
            
        except Exception as e:
            logger.error(f"Erro ao verificar existência do participante {entity_id}: {str(e)}")
            return False
    
    async def get_by_email(self, email: str) -> Optional[Participant]:        
        try:
            filter_expression = "email = :email"            
            expression_values = {":email": email}
            
            items = self.dynamodb_service.scan_table(
                self.table_name, 
                filter_expression, 
                expression_values
            )
            
            if items:
                return Participant(**items[0])
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar participante por email {email}: {str(e)}")
            raise
    
    async def get_by_cpf(self, cpf: str) -> Optional[Participant]:        
        try:
            filter_expression = "cpf = :cpf"
            expression_values = {":cpf": cpf}
            
            items = self.dynamodb_service.scan_table(
                self.table_name, 
                filter_expression, 
                expression_values
            )
            
            if items:
                return Participant(**items[0])
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar participante por CPF {cpf}: {str(e)}")
            raise
    
    async def get_by_city(self, city: str) -> List[Participant]:        
        try:
            filter_expression = "city = :city"
            expression_values = {":city": city}
            
            items = self.dynamodb_service.scan_table(
                self.table_name, 
                filter_expression, 
                expression_values
            )
            
            participants = []
            for item in items:
                participants.append(Participant(**item))
            
            return participants
            
        except Exception as e:
            logger.error(f"Erro ao buscar participantes por cidade {city}: {str(e)}")
            raise
    
    async def email_exists(self, email: str) -> bool:
        
        try:
            participant = await self.get_by_email(email)
            return participant is not None
            
        except Exception as e:
            logger.error(f"Erro ao verificar existência do email {email}: {str(e)}")
            return False
    
    async def cpf_exists(self, cpf: str) -> bool:
        
        try:
            participant = await self.get_by_cpf(cpf)
            return participant is not None
            
        except Exception as e:
            logger.error(f"Erro ao verificar existência do CPF {cpf}: {str(e)}")
            return False
