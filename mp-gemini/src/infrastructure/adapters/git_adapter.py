from typing import List, Optional
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication

# Importação robusta para evitar ImportError na v7.1
from azure.devops.v7_1.git import models as git_models
from src.domain.entities.git import GitRepository, PullRequest
from src.domain.repositories.git_repository import GitRepository as GitInterface
from config import settings


class GitAdapter(GitInterface):
    def __init__(self):
        self.personal_access_token = settings.PERSONAL_ACCESS_TOKEN
        self.organization_url = settings.ORGANIZATION_URL
        self.project_name = settings.AZURE_PROJECT_NAME

        credentials = BasicAuthentication("", self.personal_access_token)
        self.connection = Connection(base_url=self.organization_url, creds=credentials)
        self.git_client = self.connection.clients.get_git_client()

    def criar_repositorio(self, nome_repo: str) -> str:
        """Cria um repositório funcional no Azure DevOps."""
        try:
            repo_options = git_models.GitRepository(name=nome_repo)
            created = self.git_client.create_repository(
                repo_options, project=self.project_name
            )
            return f"✅ Repositório '{nome_repo}' criado. ID: {created.id}"
        except Exception as e:
            return f"❌ Erro ao criar repositório: {str(e)}"

    def create_branch(self, repo_id: str, branch_name: str) -> str:
        """Cria uma branch real baseada na main."""
        try:
            refs = self.git_client.get_refs(repository_id=repo_id, filter="heads/main")
            if not refs:
                return "❌ Erro: Branch 'main' não encontrada."

            new_ref = f"refs/heads/{branch_name}"
            ref_update = git_models.GitRefUpdate(
                name=new_ref,
                old_object_id="0000000000000000000000000000000000000000",
                new_object_id=refs[0].object_id,
            )
            self.git_client.update_refs(ref_updates=[ref_update], repository_id=repo_id)
            return f"✅ Branch '{branch_name}' criada com sucesso."
        except Exception as e:
            return f"❌ Erro ao criar branch: {str(e)}"

    def commitar_arquivos(self, repo_id: str, branch_name: str) -> str:
        """Realiza um push real de arquivo via API."""
        try:
            refs = self.git_client.get_refs(
                repository_id=repo_id, filter=f"heads/{branch_name}"
            )
            if not refs:
                return f"❌ Branch {branch_name} não encontrada."

            push = git_models.GitPush(
                ref_updates=[
                    git_models.GitRefUpdate(
                        name=f"refs/heads/{branch_name}",
                        old_object_id=refs[0].object_id,
                    )
                ],
                commits=[
                    git_models.GitCommitRef(
                        comment="MLOps: Commit automático do Agente",
                        changes=[
                            git_models.GitChange(
                                change_type="add",
                                item=git_models.ItemModel(path="/mlops_metadata.json"),
                                new_content=git_models.ItemContent(
                                    content='{"status": "deploy_ready"}',
                                    content_type="rawtext",
                                ),
                            )
                        ],
                    )
                ],
            )
            self.git_client.create_push(push, repository_id=repo_id)
            return f"✅ Arquivos commitados na branch {branch_name}."
        except Exception as e:
            return f"❌ Erro no commit: {str(e)}"

    def approve_pr(self, repo_id: str, pr_id: int) -> str:
        """Aprova o PR usando o ID do usuário autorizado."""
        try:
            user_id = self.connection.authorized_user_id
            self.git_client.create_pull_request_reviewer(
                repository_id=repo_id,
                pull_request_id=pr_id,
                reviewer_id=user_id,
                reviewer={"vote": 10},
            )
            return f"✅ PR {pr_id} aprovado."
        except Exception as e:
            return f"❌ Erro ao aprovar PR: {str(e)}"

    def merge_pr(self, repo_id: str, pr_id: int) -> str:
        """Executa o merge completo (Squash) e deleta a branch fonte."""
        try:
            pr_status = git_models.GitPullRequest(
                status="completed",
                completion_options=git_models.GitPullRequestCompletionOptions(
                    delete_source_branch=True, merge_strategy="squash"
                ),
            )
            self.git_client.update_pull_request(
                pr_status, repository_id=repo_id, pull_request_id=pr_id
            )
            return f"✅ PR {pr_id} mergeado e branch removida."
        except Exception as e:
            return f"❌ Erro no merge: {str(e)}"

    def list_repositories(self) -> List[GitRepository]:
        try:
            repos = self.git_client.get_repositories(project=self.project_name)

            if not repos:
                return []

            return [
                GitRepository(
                    id=r.id,
                    name=r.name,
                    url=r.web_url,
                    default_branch=r.default_branch if hasattr(r, "default_branch") else "main"
                )
                for r in repos
            ]

        except Exception as e:
            print(f"❌ Erro ao listar repositórios: {str(e)}")
            return []

    def get_repo(self, name: str) -> Optional[GitRepository]:
        try:
            repos = self.git_client.get_repositories(project=self.project_name)
            for r in repos:
                if r.name == name:
                    return GitRepository(
                        id=r.id,
                        name=r.name,
                        url=r.web_url,
                        default_branch=r.default_branch if hasattr(r, "default_branch") else "main"
                    )
            return None
        except Exception as e:
            print(f"❌ Erro ao buscar repositório: {str(e)}")
            return None

    def list_active_prs(self, repo_id: str) -> List[PullRequest]:
        try:
            # search_criteria=None traz apenas os ativos por padrão
            prs = self.git_client.get_pull_requests(
                repository_id=repo_id, search_criteria=None
            )
            if prs is None:
                return []

            return [
                PullRequest(
                    id=p.pull_request_id,
                    title=p.title,
                    status=p.status,
                    source_branch=p.source_ref_name.replace("refs/heads/", "") if hasattr(p, "source_ref_name") and p.source_ref_name else "",
                    target_branch=p.target_ref_name.replace("refs/heads/", "") if hasattr(p, "target_ref_name") and p.target_ref_name else ""
                )
                for p in prs
            ]
        except Exception as e:
            print(f"❌ Erro ao listar PRs (Repo ID: {repo_id}): {str(e)}")
            return []
