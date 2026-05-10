from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from src.domain.entities.git import GitRepository


@dataclass
class GitOperationResult:
    """Resultado de uma operação de Git (similar ao PaymentResult)"""

    success: bool
    message: Optional[str] = None
    pr_url: Optional[str] = None


class GitService(ABC):
    @abstractmethod
    def validate_repository_health(self, repo: GitRepository) -> bool:
        """Verifica se o repositório está pronto para receber automações"""
        pass

    @abstractmethod
    def process_automated_pr(
        self, repo: GitRepository, title: str
    ) -> GitOperationResult:
        """Orquestra a criação e validação de uma PR automatizada"""
        pass
