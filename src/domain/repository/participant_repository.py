from abc import abstractmethod
from typing import List, Optional
from src.domain.entity.participant import Participant
from src.domain.repository.base_repository import BaseRepository

class ParticipantRepository(BaseRepository[Participant]):
    """
    Repositório específico para Participant com métodos adicionais.
    Segue Clean Architecture mantendo a interface no domínio.
    """
    
    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[Participant]:
        """Busca participante por email"""
        pass
    
    @abstractmethod
    async def get_by_cpf(self, cpf: str) -> Optional[Participant]:
        """Busca participante por CPF"""
        pass
    
    @abstractmethod
    async def get_by_city(self, city: str) -> List[Participant]:
        """Busca participantes por cidade"""
        pass
    
    @abstractmethod
    async def email_exists(self, email: str) -> bool:
        """Verifica se um email já existe"""
        pass
    
    @abstractmethod
    async def cpf_exists(self, cpf: str) -> bool:
        """Verifica se um CPF já existe"""
        pass
