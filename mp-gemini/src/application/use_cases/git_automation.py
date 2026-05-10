from dataclasses import dataclass
from typing import List, Optional

# Importamos com Alias (GitEnt) para o VS Code não confundir com o Repositório
from src.domain.entities.git import GitRepository as GitEnt, PullRequest
from src.domain.repositories.git_repository import GitRepository as GitRepoInterface


@dataclass
class GitAutomationUseCase:
    """
    Orquestra as ações de Git.
    Usa o atributo .id da entidade definida em domain/entities/git.py
    """

    git_repository: GitRepoInterface

    def execute_setup_branch(self, repo_name: str, branch_name: str) -> bool:
        # Tipagem explícita 'GitEnt' garante que o editor veja o atributo .id
        repo: Optional[GitEnt] = self.git_repository.get_repo(repo_name)

        if not repo:
            raise ValueError(f"Repositório {repo_name} não encontrado.")

        # Agora o editor reconhece repo.id sem erro
        return self.git_repository.create_branch(
            repo_id=repo.id, branch_name=branch_name
        )

    def execute_approve_and_merge(self, repo_name: str, pr_id: int) -> bool:
        repo: Optional[GitEnt] = self.git_repository.get_repo(repo_name)

        if not repo:
            return False

        self.git_repository.approve_pr(repo.id, pr_id)
        return self.git_repository.merge_pr(repo.id, pr_id)

    def list_prs(self, repo_name: str) -> List[PullRequest]:
        repo: Optional[GitEnt] = self.git_repository.get_repo(repo_name)

        if not repo:
            return []

        return self.git_repository.list_active_prs(repo.id)
