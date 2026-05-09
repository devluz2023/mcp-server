from typing import List
from src.application.ports.git_service_port import GitServicePort
from src.domain.entities.git_repo import GitRepository, PullRequest


class SetupDevOpsEnvironment:
    """
    Caso de Uso responsável por orquestrar a configuração inicial
    de um ambiente DevOps seguindo o padrão GitFlow.
    """

    def __init__(self, git_service: GitServicePort):
        # Injeção de Dependência da Porta (Interface)
        self.git_service = git_service

    def execute(self, repo_name: str, file_path: str, file_content: str) -> List[PullRequest]:
        """
        Executa o fluxo de configuração:
        1. Garante que o repositório existe
        2. Cria a estrutura de branches (dev, qas, prod)
        3. Realiza o commit do arquivo inicial
        4. Lista os PRs ativos para validação
        """

        # 1. Garantir Repositório
        repo = self.git_service.get_or_create_repo(repo_name)

        # 2. Configurar GitFlow (Branches de ciclo de vida)
        # Criamos a partir da 'main'
        branches_projeto = ['dev', 'qas', 'prod']
        for branch in branches_projeto:
            self.git_service.create_branch(
                repo_id=repo.id,
                branch_name=branch,
                source_branch='main'
            )

        # 3. Versionar o arquivo solicitado
        # O conteúdo vem como string, mantendo o Use Case puro de IO de disco
        self.git_service.commit_content(
            repo_id=repo.id,
            path=file_path,
            content=file_content,
            branch='main'
        )

        # 4. Retornar Pull Requests ativos para o dashboard/interface
        return self.git_service.list_active_prs(repo.id)
