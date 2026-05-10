from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.git import GitRepository, PullRequest


class GitRepository(ABC):
    """
    Interface de Domínio (Porta de Saída).
    Define o contrato para operações de Git sem depender de provedor (GitHub/Azure).
    """

    @abstractmethod
    def get_repo(self, name: str) -> Optional[GitRepository]:
        """Busca um repositório pelo nome e retorna a Entidade."""
        pass

    @abstractmethod
    def create_branch(self, repo_id: str, branch_name: str) -> bool:
        """Cria uma branch usando o ID do repositório."""
        pass

    @abstractmethod
    def approve_pr(self, repo_id: str, pr_id: int) -> bool:
        """Aprova uma Pull Request específica."""
        pass

    @abstractmethod
    def merge_pr(self, repo_id: str, pr_id: int) -> bool:
        """Finaliza e faz o merge de uma Pull Request."""
        pass

    @abstractmethod
    def list_active_prs(self, repo_id: str) -> List[PullRequest]:
        """Retorna a lista de PRs abertas no repositório."""
        pass
