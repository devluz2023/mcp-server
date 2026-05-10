from dataclasses import dataclass
from typing import Optional


@dataclass
class GitRepository:
    """
    Entidade de Domínio que representa um repositório Git.
    O campo 'id' é essencial para as chamadas de infraestrutura.
    """

    id: str
    name: str
    url: Optional[str] = None
    default_branch: str = "main"


@dataclass
class PullRequest:
    """
    Entidade de Domínio que representa um Pull Request.
    """

    id: int
    title: str
    source_branch: str
    target_branch: str
    status: str  # ex: "open", "merged", "closed"
    author: Optional[str] = None
