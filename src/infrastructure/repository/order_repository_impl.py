import json
import logging
from typing import List, Optional
from src.domain.entity.order import Order
from src.domain.repository.order_repository import OrderRepository
from src.infrastructure.aws.dynamodb_service import DynamoDBService

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class OrderRepositoryImpl(OrderRepository):
    def __init__(self, dynamodb_service: DynamoDBService, table_name: str = "orders"):
        self.dynamodb_service = dynamodb_service
        self.table_name = table_name
    
    def create(self, entity: Order) -> Order:

        try:
            item = entity.model_dump()
            self.dynamodb_service.put_item(item, self.table_name)
            return entity
            
        except Exception as e:
            logger.error(f"Erro ao criar pedido: {str(e)}")
            raise
    
    def get_by_id(self, entity_id: int) -> Optional[Order]:
        
        try:
            key = {"order_id": entity_id}
            item = self.dynamodb_service.get_item(key, self.table_name)            
            if item:
                return Order(**item)
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar pedido por ID {entity_id}: {str(e)}")
            raise
    
    def get_all(self) -> List[Order]:
        
        try:
            items = self.dynamodb_service.scan_table(self.table_name)
            orders = []
            
            for item in items:
                orders.append(Order(**item))
            
            return orders
            
        except Exception as e:
            logger.error(f"Erro ao buscar todos os pedidos: {str(e)}")
            raise
    
    def update(self, entity_id: int, entity: Order) -> Optional[Order]:
        
        try:
            if not self.exists(entity_id):
                return None
            
            update_data = entity.model_dump()
            
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
            key = {"order_id": entity_id}
            response = self.dynamodb_service.update_item(
                key,
                update_expression,
                expression_values,
                self.table_name
            )
            
            if 'Attributes' in response:
                return Order(**response['Attributes'])
            return None
            
        except Exception as e:
            logger.error(f"Erro ao atualizar pedido {entity_id}: {str(e)}")
            raise
    
    def delete(self, entity_id: int) -> bool:
        
        try:
            key = {"order_id": entity_id}
            self.dynamodb_service.delete_item(key, self.table_name)
            return True
            
        except Exception as e:
            logger.error(f"Erro ao remover pedido {entity_id}: {str(e)}")
            return False
    
    def exists(self, entity_id: int) -> bool:
        
        try:
            key = {"order_id": entity_id}
            item = self.dynamodb_service.get_item(key, self.table_name)
            return item is not None
            
        except Exception as e:
            logger.error(f"Erro ao verificar existência do pedido {entity_id}: {str(e)}")
            return False
    
    def get_by_order_id(self, order_id: int) -> Optional[Order]:
        
        try:
            filter_expression = "orderId = :order_id"
            expression_values = {":order_id": order_id}
            
            items = self.dynamodb_service.scan_table(
                self.table_name, 
                filter_expression, 
                expression_values
            )
            
            if items:
                return Order(**items[0])
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar pedido por order_id {order_id}: {str(e)}")
            raise
    
    def get_by_participant_email(self, email: str) -> List[Order]:
        
        try:
            filter_expression = "participantEmail = :email"
            expression_values = {":email": email}
            
            items = self.dynamodb_service.scan_table(
                self.table_name, 
                filter_expression, 
                expression_values
            )
            
            orders = []
            for item in items:
                orders.append(Order(**item))
            
            return orders
            
        except Exception as e:
            logger.error(f"Erro ao buscar pedidos por email {email}: {str(e)}")
            raise
    
    def get_by_product_id(self, product_id: int) -> List[Order]:
        
        try:
            filter_expression = "productId = :product_id"
            expression_values = {":product_id": product_id}
            
            items = self.dynamodb_service.scan_table(
                self.table_name, 
                filter_expression, 
                expression_values
            )
            
            orders = []
            for item in items:
                orders.append(Order(**item))
            
            return orders
            
        except Exception as e:
            logger.error(f"Erro ao buscar pedidos por product_id {product_id}: {str(e)}")
            raise
    
    def get_orders_by_date_range(self, start_date: str, end_date: str) -> List[Order]:
        
        try:
            filter_expression = "orderDate BETWEEN :start_date AND :end_date"
            expression_values = {
                ":start_date": start_date,
                ":end_date": end_date
            }
            
            items = self.dynamodb_service.scan_table(
                self.table_name, 
                filter_expression, 
                expression_values
            )
            
            orders = []
            for item in items:
                orders.append(Order(**item))
            
            return orders
            
        except Exception as e:
            logger.error(f"Erro ao buscar pedidos por intervalo de datas {start_date} - {end_date}: {str(e)}")
            raise
