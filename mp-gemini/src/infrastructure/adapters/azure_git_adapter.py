import os
import logging
from typing import List, Optional

from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.exceptions import AzureDevOpsServiceError
from azure.devops.v7_1.git.models import (
    GitPullRequestSearchCriteria,
    GitPullRequestCompletionOptions,
    GitPush,
    GitCommitRef
)

from src.application.ports.git_service_port import GitServicePort
from src.domain.entities.git_repo import GitRepository, PullRequest

logger = logging.getLogger(__name__)

class AzureGitAdapter(GitServicePort):
    def __init__(self):
        self.pat = os.getenv('PERSONAL_ACCESS_TOKEN')
        self.org_url = os.getenv('ORGANIZATION_URL')
        self.project = os.getenv('PROJECT_NAME')

        if not all([self.pat, self.org_url, self.project]):
            raise ValueError("Credenciais Azure DevOps não configuradas no .env")

        credentials = BasicAuthentication('', self.pat)
        self.connection = Connection(base_url=self.org_url, creds=credentials)
        self.client = self.connection.clients.get_git_client()
        self._meu_id = None

    @property
    def meu_id(self):
        """Lazy load do ID do usuário autenticado"""
        if not self._meu_id:
            config_client = self.connection.clients.get_location_client()
            connection_data = config_client.get_connection_data()
            self._meu_id = connection_data.authenticated_user.id
        return self._meu_id

    def get_or_create_repo(self, name: str) -> GitRepository:
        try:
            repo = self.client.get_repository(repository_id=name, project=self.project)
            logger.info(f"Repositório encontrado: {repo.name}")
        except AzureDevOpsServiceError:
            logger.info(f"Criando repositório: {name}")
            repo = self.client.create_repository({'name': name}, project=self.project)

        return GitRepository(id=repo.id, name=repo.name)

    def create_branch(self, repo_id: str, branch_name: str, source_branch: str = "main") -> bool:
        try:
            # Busca o SHA da branch base
            refs = self.client.get_refs(repository_id=repo_id, project=self.project, filter=f"heads/{source_branch}")
            if not refs:
                logger.error(f"Branch base {source_branch} não encontrada.")
                return False

            base_sha = refs[0].object_id
            new_ref = [{
                "name": f"refs/heads/{branch_name}",
                "oldObjectId": "0000000000000000000000000000000000000000",
                "newObjectId": base_sha
            }]

            self.client.update_refs(new_ref, repository_id=repo_id, project=self.project)
            return True
        except AzureDevOpsServiceError as e:
            if "already exists" in str(e):
                return True
            logger.error(f"Erro ao criar branch {branch_name}: {e}")
            return False

    def commit_file(self, repo_id: str, path: str, content: str, branch: str) -> bool:
        try:
            # Tenta obter o SHA atual da branch para o push
            ref_name = f"heads/{branch}"
            refs = self.client.get_refs(repository_id=repo_id, project=self.project, filter=ref_name)
            old_object_id = refs[0].object_id if refs else "0000000000000000000000000000000000000000"

            push = {
                'commits': [{
                    'comment': f'Upload de {path} via Clean Architecture',
                    'changes': [{
                        'changeType': 'add', # Pode ser edit se o arquivo já existir
                        'item': {'path': f'/{path}'},
                        'newContent': {'content': content, 'contentType': 'rawText'}
                    }]
                }],
                'refUpdates': [{
                    'name': f'refs/heads/{branch}',
                    'oldObjectId': old_object_id
                }]
            }

            self.client.create_push(push, repository_id=repo_id, project=self.project)
            return True
        except Exception as e:
            logger.error(f"Falha no commit: {e}")
            return False

    def list_active_prs(self, repo_id: str) -> List[PullRequest]:
        search_criteria = GitPullRequestSearchCriteria(status='active')
        prs = self.client.get_pull_requests(repo_id, search_criteria, project=self.project)

        return [
            PullRequest(
                id=p.pull_request_id,
                title=p.title,
                source_branch=p.source_ref_name,
                target_branch=p.target_ref_name,
                status=p.status
            ) for p in prs
        ]

    def approve_pr(self, repo_id: str, pr_id: int) -> bool:
        try:
            vote = {"vote": 10, "id": self.meu_id}
            self.client.create_pull_request_reviewer(
                vote, repository_id=repo_id, pull_request_id=pr_id,
                reviewer_id=self.meu_id, project=self.project
            )
            return True
        except Exception as e:
            logger.error(f"Erro ao votar no PR {pr_id}: {e}")
            return False

    def merge_pr(self, repo_id: str, pr_id: int, source_commit: str) -> bool:
        try:
            options = GitPullRequestCompletionOptions(
                delete_source_branch=True,
                squash_merge=True
            )
            pr_update = {
                "status": "completed",
                "lastMergeSourceCommit": {"commitId": source_commit},
                "completionOptions": options
            }
            self.client.update_pull_request(
                pr_update, repository_id=repo_id, pull_request_id=pr_id, project=self.project
            )
            return True
        except Exception as e:
            logger.error(f"Erro no merge do PR {pr_id}: {e}")
            return False
