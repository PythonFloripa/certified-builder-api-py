import logging
import json
from botocore.exceptions import ClientError
from typing import Dict, List, Optional, Any
from decimal import Decimal

from src.infrastructure.aws.boto_aws import get_instance_aws, ServiceNameAWS

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class DynamoDBService:
    """
    Serviço para operações com DynamoDB.
    Implementa operações CRUD básicas e métodos específicos para cada entidade.
    """
    
    def __init__(self):
        self.aws = get_instance_aws(ServiceNameAWS.DYNAMODB)

    def put_item(self, item: Dict, table_name: str) -> Dict:
        """
        Adiciona um item na tabela DynamoDB.
        
        Args:
            item: Item a ser adicionado
            table_name: Nome da tabela
            
        Returns:
            Dict: Resposta da operação
        """
        try:
            # Converte valores para Decimal para compatibilidade com DynamoDB
            item = self._convert_to_dynamodb_format(item)
            
            logger.info(f"Adicionando item na tabela {table_name}: {item}")
            response = self.aws.put_item(
                TableName=table_name,
                Item=item
            )
            logger.info(f"Item adicionado com sucesso: {response}")
            return response
        except ClientError as e:
            logger.error(f"Erro ao adicionar item na tabela {table_name}: {str(e)}")
            raise

    def get_item(self, key: Dict, table_name: str) -> Optional[Dict]:
        """
        Busca um item na tabela DynamoDB.
        
        Args:
            key: Chave primária do item
            table_name: Nome da tabela
            
        Returns:
            Optional[Dict]: Item encontrado ou None
        """
        try:
            logger.info(f"Buscando item na tabela {table_name} com chave: {key}")
            response = self.aws.get_item(
                TableName=table_name,
                Key=key
            )
            
            if 'Item' in response:
                item = self._convert_from_dynamodb_format(response['Item'])
                logger.info(f"Item encontrado: {item}")
                return item
            else:
                logger.info(f"Item não encontrado na tabela {table_name}")
                return None
                
        except ClientError as e:
            logger.error(f"Erro ao buscar item na tabela {table_name}: {str(e)}")
            raise

    def update_item(self, key: Dict, update_expression: str, expression_values: Dict, table_name: str) -> Dict:
        """
        Atualiza um item na tabela DynamoDB.
        
        Args:
            key: Chave primária do item
            update_expression: Expressão de atualização
            expression_values: Valores para a expressão
            table_name: Nome da tabela
            
        Returns:
            Dict: Resposta da operação
        """
        try:
            # Converte valores para Decimal
            expression_values = self._convert_to_dynamodb_format(expression_values)
            
            logger.info(f"Atualizando item na tabela {table_name} com chave: {key}")
            response = self.aws.update_item(
                TableName=table_name,
                Key=key,
                UpdateExpression=update_expression,
                ExpressionAttributeValues=expression_values,
                ReturnValues="ALL_NEW"
            )
            logger.info(f"Item atualizado com sucesso: {response}")
            return response
        except ClientError as e:
            logger.error(f"Erro ao atualizar item na tabela {table_name}: {str(e)}")
            raise

    def delete_item(self, key: Dict, table_name: str) -> Dict:
        """
        Remove um item da tabela DynamoDB.
        
        Args:
            key: Chave primária do item
            table_name: Nome da tabela
            
        Returns:
            Dict: Resposta da operação
        """
        try:
            logger.info(f"Removendo item da tabela {table_name} com chave: {key}")
            response = self.aws.delete_item(
                TableName=table_name,
                Key=key
            )
            logger.info(f"Item removido com sucesso: {response}")
            return response
        except ClientError as e:
            logger.error(f"Erro ao remover item da tabela {table_name}: {str(e)}")
            raise

    def scan_table(self, table_name: str, filter_expression: str = None, expression_values: Dict = None) -> List[Dict]:
        """
        Escaneia uma tabela DynamoDB.
        
        Args:
            table_name: Nome da tabela
            filter_expression: Expressão de filtro (opcional)
            expression_values: Valores para a expressão (opcional)
            
        Returns:
            List[Dict]: Lista de itens encontrados
        """
        try:
            scan_kwargs = {'TableName': table_name}
            
            if filter_expression and expression_values:
                expression_values = self._convert_to_dynamodb_format(expression_values)
                scan_kwargs['FilterExpression'] = filter_expression
                scan_kwargs['ExpressionAttributeValues'] = expression_values
            
            logger.info(f"Escaneando tabela {table_name}")
            response = self.aws.scan(**scan_kwargs)
            
            items = []
            if 'Items' in response:
                for item in response['Items']:
                    items.append(self._convert_from_dynamodb_format(item))
            
            logger.info(f"Encontrados {len(items)} itens na tabela {table_name}")
            return items
            
        except ClientError as e:
            logger.error(f"Erro ao escanear tabela {table_name}: {str(e)}")
            raise

    def query_table(self, table_name: str, key_condition_expression: str, expression_values: Dict) -> List[Dict]:
        """
        Consulta uma tabela DynamoDB.
        
        Args:
            table_name: Nome da tabela
            key_condition_expression: Expressão de condição da chave
            expression_values: Valores para a expressão
            
        Returns:
            List[Dict]: Lista de itens encontrados
        """
        try:
            expression_values = self._convert_to_dynamodb_format(expression_values)
            
            logger.info(f"Consultando tabela {table_name} com expressão: {key_condition_expression}")
            response = self.aws.query(
                TableName=table_name,
                KeyConditionExpression=key_condition_expression,
                ExpressionAttributeValues=expression_values
            )
            
            items = []
            if 'Items' in response:
                for item in response['Items']:
                    items.append(self._convert_from_dynamodb_format(item))
            
            logger.info(f"Encontrados {len(items)} itens na consulta")
            return items
            
        except ClientError as e:
            logger.error(f"Erro ao consultar tabela {table_name}: {str(e)}")
            raise

    def _convert_to_dynamodb_format(self, data: Any) -> Any:
        """
        Converte dados para o formato aceito pelo DynamoDB.
        Quando usando boto3.client('dynamodb'), strings devem ser convertidas para {'S': 'valor'}.
        
        Args:
            data: Dados a serem convertidos
            
        Returns:
            Any: Dados convertidos no formato JSON do DynamoDB
        """
        if isinstance(data, dict):
            return {k: self._convert_to_dynamodb_format(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._convert_to_dynamodb_format(item) for item in data]
        elif isinstance(data, str):
            # Converte strings para o formato JSON do DynamoDB: {'S': 'valor'}
            return {'S': data}
        elif isinstance(data, (int, float)) and not isinstance(data, bool):
            # Converte números para o formato JSON do DynamoDB: {'N': 'valor'}
            return {'N': str(data)}
        elif isinstance(data, bool):
            # Converte booleanos para o formato JSON do DynamoDB: {'BOOL': valor}
            return {'BOOL': data}
        else:
            return data

    def _convert_from_dynamodb_format(self, data: Any) -> Any:
        """
        Converte dados do formato DynamoDB para Python.
        Converte o formato JSON do DynamoDB ({'S': 'valor'}, {'N': '123'}) para tipos Python.
        
        Args:
            data: Dados a serem convertidos
            
        Returns:
            Any: Dados convertidos para tipos Python
        """
        if isinstance(data, dict):
            # Verifica se é um formato JSON do DynamoDB
            if len(data) == 1:
                key = list(data.keys())[0]
                if key == 'S':  # String
                    return data['S']
                elif key == 'N':  # Número
                    return float(data['N'])
                elif key == 'BOOL':  # Booleano
                    return data['BOOL']
                elif key == 'L':  # Lista
                    return [self._convert_from_dynamodb_format(item) for item in data['L']]
                elif key == 'M':  # Mapa
                    return {k: self._convert_from_dynamodb_format(v) for k, v in data['M'].items()}
                elif key == 'NULL':  # Null
                    return None
            
            # Se não for formato JSON do DynamoDB, processa normalmente
            return {k: self._convert_from_dynamodb_format(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._convert_from_dynamodb_format(item) for item in data]
        elif isinstance(data, Decimal):
            return float(data)
        else:
            return data




