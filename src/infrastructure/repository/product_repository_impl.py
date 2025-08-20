import json
import logging
from typing import List, Optional
from src.domain.entity.product import Product
from src.domain.repository.product_repository import ProductRepository
from src.infrastructure.aws.dynamodb_service import DynamoDBService

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class ProductRepositoryImpl(ProductRepository):
    
    def __init__(self, dynamodb_service: DynamoDBService, table_name: str = "products"):
        self.dynamodb_service = dynamodb_service
        self.table_name = table_name
    
    async def create(self, entity: Product) -> Product:
        
        try:
            item = entity.model_dump()
            self.dynamodb_service.put_item(item, self.table_name)
            
            return entity
            
        except Exception as e:
            logger.error(f"Erro ao criar produto: {str(e)}")
            raise
    
    async def get_by_id(self, entity_id: int) -> Optional[Product]:
        
        try:
            # Usa product_id como chave primária conforme definido no schema da tabela
            key = {"product_id": entity_id}
            item = self.dynamodb_service.get_item(key, self.table_name)
            
            if item:
                return Product(**item)
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar produto por ID {entity_id}: {str(e)}")
            raise
    
    async def get_all(self) -> List[Product]:
        try:
            items = self.dynamodb_service.scan_table(self.table_name)
            products = []
            
            for item in items:
                products.append(Product(**item))
            
            return products
            
        except Exception as e:
            logger.error(f"Erro ao buscar todos os produtos: {str(e)}")
            raise
    
    async def update(self, entity_id: int, entity: Product) -> Optional[Product]:
        
        try:
            # Verifica se o produto existe
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
            key = {"product_id": entity_id}
            response = self.dynamodb_service.update_item(
                key,
                update_expression,
                expression_values,
                self.table_name
            )
            
            if 'Attributes' in response:
                return Product(**response['Attributes'])
            return None
            
        except Exception as e:
            logger.error(f"Erro ao atualizar produto {entity_id}: {str(e)}")
            raise
    
    async def delete(self, entity_id: int) -> bool:
        
        try:
            key = {"product_id": entity_id}
            self.dynamodb_service.delete_item(key, self.table_name)
        
            return True
            
        except Exception as e:
            logger.error(f"Erro ao remover produto {entity_id}: {str(e)}")
            return False
    
    async def exists(self, entity_id: int) -> bool:        
        try:
            key = {"product_id": entity_id}
            item = self.dynamodb_service.get_item(key, self.table_name)
            return item is not None
            
        except Exception as e:
            logger.error(f"Erro ao verificar existência do produto {entity_id}: {str(e)}")
            return False
    
    async def get_by_product_id(self, product_id: int) -> Optional[Product]:
        
        try:
            filter_expression = "productId = :product_id"
            expression_values = {":product_id": product_id}
            
            items = self.dynamodb_service.scan_table(
                self.table_name, 
                filter_expression, 
                expression_values
            )
            
            if items:
                return Product(**items[0])
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar produto por product_id {product_id}: {str(e)}")
            raise
    
    async def get_by_name(self, product_name: str) -> List[Product]:
        
        try:
            filter_expression = "productName = :product_name"
            expression_values = {":product_name": product_name}
            
            items = self.dynamodb_service.scan_table(
                self.table_name, 
                filter_expression, 
                expression_values
            )
            
            products = []
            for item in items:
                products.append(Product(**item))
            
            return products
            
        except Exception as e:
            logger.error(f"Erro ao buscar produtos por nome {product_name}: {str(e)}")
            raise
    
    async def get_products_with_logo(self) -> List[Product]:
        
        try:
            filter_expression = "attribute_exists(certificateLogo)"
            
            items = self.dynamodb_service.scan_table(
                self.table_name, 
                filter_expression
            )
            
            products = []
            for item in items:
                products.append(Product(**item))
            
            return products
            
        except Exception as e:
            logger.error(f"Erro ao buscar produtos com logo: {str(e)}")
            raise
    
    async def get_products_with_background(self) -> List[Product]:
        
        try:
            filter_expression = "attribute_exists(certificateBackground)"
            
            items = self.dynamodb_service.scan_table(
                self.table_name, 
                filter_expression
            )
            
            products = []
            for item in items:
                products.append(Product(**item))
            
            return products
            
        except Exception as e:
            logger.error(f"Erro ao buscar produtos com background: {str(e)}")
            raise
