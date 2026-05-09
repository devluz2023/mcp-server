from typing import List

from src.application.ports.git_service_port import GitServicePort
from src.domain.entities.git_repo import PullRequest


class SetupDevOpsEnvironment:
    """
    Caso de Uso responsável por orquestrar a configuração inicial
    de um ambiente DevOps seguindo o padrão GitFlow.
    """

    def __init__(self, git_service: GitServicePort):
        # Injeção de Dependência da Porta (Interface)
        self.git_service = git_service

    def execute(
        self,
        repo_name: str,
        file_path: str = "README.md",
        file_content: str = "# Repositório criado com GitFlow (main, dev, qas, prod)\n",
    ) -> List[PullRequest]:
        """
        Executa o fluxo de configuração:
        1. Garante que o repositório existe
        2. Cria o commit inicial em main
        3. Cria a estrutura de branches (dev, qas, prod)
        4. Lista os PRs ativos para validação
        """

        # 1. Garantir Repositório
        repo = self.git_service.get_or_create_repo(repo_name)

        # 2. Commit inicial em main para permitir criação de branches GitFlow
        created = self.git_service.commit_content(
            repo_id=repo.id,
            path=file_path,
            content=file_content,
            branch="main",
        )
        if not created:
            raise RuntimeError(
                f"Falha ao criar commit inicial em main para o repositório '{repo_name}'."
            )

        # 3. Configurar GitFlow (branches de ciclo de vida)
        branches_projeto = ["dev", "qas", "prod"]
        created_branches = []
        for branch in branches_projeto:
            created_branches.append(
                self.git_service.create_branch(
                    repo_id=repo.id,
                    branch_name=branch,
                    source_branch="main",
                )
            )

        if not all(created_branches):
            raise RuntimeError(
                f"Falha ao criar branches GitFlow para o repositório '{repo_name}'."
            )

        # 4. Retornar Pull Requests ativos para o dashboard/interface
        return self.git_service.list_active_prs(repo.id)
