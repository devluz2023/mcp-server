from langchain.tools import tool
from src.application.use_cases.git_automation import GitAutomationUseCase

# Dicionário global para armazenar as ferramentas injetadas
_tools_registry = {}


def initialize_tools(git_uc: GitAutomationUseCase, job_uc):
    """
    Registra as ferramentas injetando os Use Cases necessários.
    """

    @tool
    def criar_branch_ml(branch_name: str):
        """Útil para criar uma nova branch de desenvolvimento no Git."""
        return git_uc.execute_setup_branch(
            repo_name="meu_repo", branch_name=branch_name
        )

    @tool
    def listar_jobs_databricks(dummy_arg: str = ""):
        """Lista todos os jobs ativos no Databricks."""
        return job_uc.execute_list_jobs()

    # Adiciona ao registro global
    _tools_registry["criar_branch_ml"] = criar_branch_ml
    _tools_registry["listar_jobs_databricks"] = listar_jobs_databricks


def get_tools():
    return _tools_registry
