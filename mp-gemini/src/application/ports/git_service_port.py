from abc import ABC, abstractmethod
from typing import List, Optional

from src.domain.entities.git_repo import GitRepository, PullRequest


class GitServicePort(ABC):
    @abstractmethod
    def get_or_create_repo(self, name: str) -> GitRepository:
        pass

    @abstractmethod
    def get_repo(self, name: str) -> Optional[GitRepository]:
        pass

    @abstractmethod
    def list_repos(self) -> List[GitRepository]:
        pass

    @abstractmethod
    def create_branch(
        self, repo_id: str, branch_name: str, source_branch: str = "main"
    ) -> bool:
        pass

    @abstractmethod
    def commit_content(
        self, repo_id: str, path: str, content: str, branch: str
    ) -> bool:
        pass

    @abstractmethod
    def list_active_prs(self, repo_id: str) -> list[PullRequest]:
        pass

    @abstractmethod
    def approve_pr(self, repo_id: str, pr_id: int) -> bool:
        pass

    @abstractmethod
    def merge_pr(self, repo_id: str, pr_id: int) -> bool:
        pass
