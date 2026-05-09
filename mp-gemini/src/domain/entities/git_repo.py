# src/domain/entities/git_repo.py
from dataclasses import dataclass


@dataclass
class GitRepository:
    id: str
    name: str


@dataclass
class PullRequest:
    id: int
    title: str
    source_branch: str
    target_branch: str
    status: str
