from typing import List, Optional

from src.application.ports.git_service_port import GitServicePort
from src.domain.entities.git_repo import GitRepository, PullRequest


class GitRepositoryUseCase:
    def __init__(self, git_service: GitServicePort):
        self.git_service = git_service

    def list_repositories(self) -> List[GitRepository]:
        return self.git_service.list_repos()

    def get_repository(self, name: str) -> Optional[GitRepository]:
        return self.git_service.get_repo(name)

    def commit_and_push(
        self, repo_name: str, path: str, content: str, branch: str = "main"
    ) -> bool:
        repo = self.git_service.get_or_create_repo(repo_name)
        return self.git_service.commit_content(repo.id, path, content, branch)

    def list_active_pull_requests(self, repo_name: str) -> List[PullRequest]:
        repo = self.get_repository(repo_name)
        if not repo:
            raise ValueError(f"Repositório '{repo_name}' não encontrado.")
        return self.git_service.list_active_prs(repo.id)

    def approve_pull_request(self, repo_name: str, pr_id: int) -> bool:
        repo = self.get_repository(repo_name)
        if not repo:
            raise ValueError(f"Repositório '{repo_name}' não encontrado.")
        return self.git_service.approve_pr(repo.id, pr_id)

    def merge_pull_request(self, repo_name: str, pr_id: int) -> bool:
        repo = self.get_repository(repo_name)
        if not repo:
            raise ValueError(f"Repositório '{repo_name}' não encontrado.")
        return self.git_service.merge_pr(repo.id, pr_id)

    def create_branch(
        self,
        repo_name: str,
        branch_name: str,
        source_branch: str = "main",
    ) -> bool:
        repo = self.get_repository(repo_name)
        if not repo:
            raise ValueError(f"Repositório '{repo_name}' não encontrado.")
        return self.git_service.create_branch(
            repo_id=repo.id, branch_name=branch_name, source_branch=source_branch
        )
