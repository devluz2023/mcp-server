# src/application/ports/git_service_port.py
from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.git_repo import GitRepository, PullRequest

class GitServicePort(ABC):
    @abstractmethod
    def get_or_create_repo(self, name: str) -> GitRepository: pass

    @abstractmethod
    def create_branch(self, repo_id: str, branch_name: str, source_branch: str) -> bool: pass

    @abstractmethod
    def commit_file(self, repo_id: str, path: str, content: str, branch: str) -> bool: pass

    @abstractmethod
    def list_active_prs(self, repo_id: str) -> List[PullRequest]: pass

    @abstractmethod
    def approve_and_merge_pr(self, pr_id: int) -> bool: pass


    @abstractmethod
    def approve_pr(self, repo_id: str, pr_id: int) -> bool:
        pass
