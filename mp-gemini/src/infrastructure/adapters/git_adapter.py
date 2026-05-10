from typing import List, Optional
from src.domain.entities.git import GitRepository, PullRequest
from src.domain.repositories.git_repository import GitRepository as GitInterface
from config import settings


class GitAdapter(GitInterface):
    def __init__(self):
        self.token = settings.PERSONAL_ACCESS_TOKEN
        self.org_url = settings.ORGANIZATION_URL

    def get_repo(self, name: str) -> Optional[GitRepository]:
        return GitRepository(
            id="guid-repo-123", name=name, url=f"{self.org_url}/{name}"
        )

    def create_branch(self, repo_id: str, branch_name: str) -> bool:
        print(f"Infra: Criando branch {branch_name}")
        return True

    def list_active_prs(self, repo_id: str) -> List[PullRequest]:
        return []

    # --- ADICIONE ESTES MÉTODOS ---
    def approve_pr(self, repo_id: str, pr_id: int) -> bool:
        print(f"Aprovando PR {pr_id}")
        return True

    def merge_pr(self, repo_id: str, pr_id: int) -> bool:
        print(f"Mergeando PR {pr_id}")
        return True
