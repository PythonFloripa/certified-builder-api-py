"""
Container de Dependências para centralizar a injeção de dependências.
Segue o padrão Dependency Injection Container para Clean Architecture.
"""

from typing import Dict, Any
from src.infrastructure.aws.dynamodb_service import DynamoDBService
from src.infrastructure.aws.sqs_service import SQSService
from src.infrastructure.repository.certificate_repository_impl import CertificateRepositoryImpl
from src.infrastructure.repository.participant_repository_impl import ParticipantRepositoryImpl
from src.infrastructure.repository.product_repository_impl import ProductRepositoryImpl
from src.infrastructure.repository.order_repository_impl import OrderRepositoryImpl


class DependencyContainer:
    """
    Container de dependências que centraliza a criação e injeção de dependências.
    Segue o padrão Singleton para garantir uma única instância.
    """
    
    _instance = None
    _services: Dict[str, Any] = {}
    _singletons: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DependencyContainer, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not self._services:
            self._register_services()
    
    def _register_services(self):
        """
        Registra todos os serviços no container.
        Define como cada dependência deve ser criada.
        """
        # Registra serviços de infraestrutura
        self._services['dynamodb_service'] = self._create_dynamodb_service
        self._services['sqs_service'] = self._create_sqs_service
        # Registra repositórios
        self._services['certificate_repository'] = self._create_certificate_repository
        self._services['participant_repository'] = self._create_participant_repository
        self._services['product_repository'] = self._create_product_repository
        self._services['order_repository'] = self._create_order_repository
    
    def get(self, service_name: str) -> Any:
        """
        Obtém uma instância do serviço solicitado.
        Cria singleton automaticamente se necessário.
        
        Args:
            service_name: Nome do serviço registrado
            
        Returns:
            Any: Instância do serviço
        """
        if service_name not in self._services:
            raise ValueError(f"Serviço '{service_name}' não registrado no container")
        
        # Verifica se já existe uma instância singleton
        if service_name in self._singletons:
            return self._singletons[service_name]
        
        # Cria nova instância
        instance = self._services[service_name]()
        
        # Armazena como singleton se necessário
        self._singletons[service_name] = instance
        
        return instance
    
    def reset(self):
        """
        Reseta o container, removendo todas as instâncias singleton.
        Útil para testes.
        """
        self._singletons.clear()
    
    def _create_sqs_service(self) -> SQSService:
        """Cria uma instância do SQSService."""
        return SQSService()

    # Métodos de criação de serviços de infraestrutura
    def _create_dynamodb_service(self) -> DynamoDBService:
        """Cria uma instância do DynamoDBService."""
        return DynamoDBService()
    
    # Métodos de criação de repositórios
    def _create_certificate_repository(self) -> CertificateRepositoryImpl:
        """Cria uma instância do CertificateRepositoryImpl."""
        dynamodb_service = self.get('dynamodb_service')
        return CertificateRepositoryImpl(dynamodb_service, "certificates")
    
    def _create_participant_repository(self) -> ParticipantRepositoryImpl:
        """Cria uma instância do ParticipantRepositoryImpl."""
        dynamodb_service = self.get('dynamodb_service')
        return ParticipantRepositoryImpl(dynamodb_service, "participants")
    
    def _create_product_repository(self) -> ProductRepositoryImpl:
        """Cria uma instância do ProductRepositoryImpl."""
        dynamodb_service = self.get('dynamodb_service')
        return ProductRepositoryImpl(dynamodb_service, "products")
    
    def _create_order_repository(self) -> OrderRepositoryImpl:
        """Cria uma instância do OrderRepositoryImpl."""
        dynamodb_service = self.get('dynamodb_service')
        return OrderRepositoryImpl(dynamodb_service, "orders")
    

# Instância global do container
container = DependencyContainer()
