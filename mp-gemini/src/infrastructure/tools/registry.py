import os

from langchain_core.tools import tool
from src.domain.use_cases.git_repository_use_case import GitRepositoryUseCase
from src.domain.use_cases.setup_devops_environment import SetupDevOpsEnvironment
from src.infrastructure.adapters.azure_git_adapter import AzureGitAdapter
from src.infrastructure.repositories.databricks_job_repository import (
    DatabricksJobRepository,
)

db = DatabricksJobRepository()

git_adapter = AzureGitAdapter()
git_use_case = GitRepositoryUseCase(git_service=git_adapter)
setup_devops_use_case = SetupDevOpsEnvironment(git_service=git_adapter)


@tool
def listar_jobs_databricks() -> str:
    """Lista jobs no Databricks"""
    return db.listar_jobs()


@tool
def executar_job_databricks(job_id: int) -> str:
    """Executa job no Databricks"""
    return db.executar_job(job_id)


@tool
def criar_job_databricks(nome: str) -> str:
    """Cria job no Databricks"""
    return db.criar_job(nome)


@tool
def atualizar_job_databricks(job_id: int, novo_nome: str) -> str:
    """Atualiza job no Databricks"""
    return db.atualizar_job(job_id, novo_nome)


@tool
def deletar_job_databricks(job_id: int) -> str:
    """Deleta job no Databricks"""
    return db.deletar_job(job_id)


@tool
def criar_dashboard_databricks() -> str:
    """Cria dashboard no Databricks"""
    return db.criar_dashboard_padrao()


@tool
def show_drift() -> str:
    """Mostra os drifts"""
    return db.show_drift()


@tool
def bundle_job_yaml() -> str:
    """Cria bundle yaml"""
    return db.bundle_job_yaml()


@tool
def pipeline_databricks() -> str:
    """
    Pipeline completo: CSV → Delta → Feature Store
    """
    return db.executar_pipeline_csv_para_feature_store()


@tool
def deploy_modelo_databricks(nome_modelo: str) -> str:
    """Faz deploy de modelo Python"""
    return db.deploy_modelo(nome_modelo)


@tool
def listar_modelos() -> str:
    """Lista modelos locais"""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, "..", "models")

    return "\n".join([f for f in os.listdir(models_dir) if f.endswith(".py")])


@tool
def listar_repositorios() -> str:
    """Lista repositórios no Azure DevOps"""
    repos = git_use_case.list_repositories()
    if not repos:
        return "Nenhum repositório encontrado."
    return "\n".join([f"- {repo.name} (ID: {repo.id})" for repo in repos])


@tool
def commit_e_push_arquivo(
    repo_name: str, arquivo: str, conteudo: str, branch: str = "main"
) -> str:
    """Faz commit e push de um arquivo para o repositório especificado.

    O caminho do arquivo pode incluir pastas, por exemplo: 'modelo/meu_arquivo.py'.
    """
    success = git_use_case.commit_and_push(repo_name, arquivo, conteudo, branch)
    if not success:
        return f"Falha ao commitar/push no repositório '{repo_name}' branch '{branch}'."
    return f"Commit e push realizados com sucesso em '{repo_name}' branch '{branch}'."


@tool
def versionar_arquivo(
    repo_name: str, caminho: str, conteudo: str, branch: str = "main"
) -> str:
    """Versiona um arquivo em uma pasta do repositório."""
    success = git_use_case.commit_and_push(repo_name, caminho, conteudo, branch)
    if not success:
        return (
            f"Falha ao versionar o arquivo '{caminho}' no repositório '{repo_name}' "
            f"branch '{branch}'."
        )
    return f"Arquivo '{caminho}' versionado e enviado com sucesso em '{repo_name}' branch '{branch}'."


@tool
def versionar_arquivo_models(
    repo_name: str, filename: str, conteudo: str, branch: str = "main"
) -> str:
    """Versiona um arquivo dentro da pasta models em um branch especificado."""
    caminho = filename if filename.startswith("models/") else f"models/{filename}"
    success = git_use_case.commit_and_push(repo_name, caminho, conteudo, branch)
    if not success:
        return (
            f"Falha ao versionar o arquivo '{caminho}' no repositório '{repo_name}' "
            f"branch '{branch}'."
        )
    return f"Arquivo '{caminho}' versionado e enviado com sucesso em '{repo_name}' branch '{branch}'."


@tool
def listar_prs(repo_name: str) -> str:
    """Lista Pull Requests ativos para um repositório."""
    try:
        prs = git_use_case.list_active_pull_requests(repo_name)
    except ValueError as exc:
        return str(exc)

    if not prs:
        return f"Nenhum Pull Request ativo encontrado em '{repo_name}'."
    lines = [
        f"- PR #{pr.id}: {pr.title} | {pr.source_branch} → {pr.target_branch} | {pr.status}"
        for pr in prs
    ]
    return "\n".join(lines)


@tool
def aprovar_pr(repo_name: str, pr_id: int) -> str:
    """Aprova um Pull Request existente."""
    try:
        approved = git_use_case.approve_pull_request(repo_name, pr_id)
    except ValueError as exc:
        return str(exc)
    return (
        f"PR #{pr_id} aprovado com sucesso."
        if approved
        else f"Falha ao aprovar PR #{pr_id}."
    )


@tool
def merge_pr(repo_name: str, pr_id: int) -> str:
    """Faz merge de um Pull Request existente."""
    try:
        merged = git_use_case.merge_pull_request(repo_name, pr_id)
    except ValueError as exc:
        return str(exc)
    return (
        f"PR #{pr_id} mergeada com sucesso."
        if merged
        else f"Falha ao mergear PR #{pr_id}."
    )


@tool
def criar_branch(
    repo_name: str,
    branch_name: str,
    source_branch: str = "main",
) -> str:
    """Cria uma nova branch a partir de uma branch base."""
    try:
        created = git_use_case.create_branch(repo_name, branch_name, source_branch)
    except ValueError as exc:
        return str(exc)
    return (
        f"Branch '{branch_name}' criada com sucesso em '{repo_name}' a partir de '{source_branch}'."
        if created
        else f"Falha ao criar branch '{branch_name}' em '{repo_name}'."
    )


@tool
def criar_repositorio_gitflow(
    repo_name: str,
    initial_file: str = "README.md",
    content: str = "# Repositório criado com GitFlow (main, dev, qas, prod)\n",
) -> str:
    """Cria um repositório e configura GitFlow com branches dev, qas e prod."""
    try:
        prs = setup_devops_use_case.execute(
            repo_name=repo_name,
            file_path=initial_file,
            file_content=content,
        )
    except Exception as exc:
        return f"Falha ao criar repositório GitFlow: {exc}"

    if prs:
        return (
            f"Repositório '{repo_name}' criado com GitFlow e branches dev/qas/prod. "
            f"{len(prs)} PRs ativos encontrados."
        )

    return (
        f"Repositório '{repo_name}' criado com GitFlow com sucesso e nenhum PR ativo."
    )


# =========================
# TOOL REGISTRY (IMPORTANTE)
# =========================
tools = {
    "listar_jobs_databricks": listar_jobs_databricks,
    "executar_job_databricks": executar_job_databricks,
    "criar_job_databricks": criar_job_databricks,
    "atualizar_job_databricks": atualizar_job_databricks,
    "deletar_job_databricks": deletar_job_databricks,
    "criar_dashboard_databricks": criar_dashboard_databricks,
    "deploy_modelo_databricks": deploy_modelo_databricks,
    "listar_modelos": listar_modelos,
    "pipeline_databricks": pipeline_databricks,
    "bundle_job_yaml": bundle_job_yaml,
    "show_drift": show_drift,
    "listar_repositorios": listar_repositorios,
    "commit_e_push_arquivo": commit_e_push_arquivo,
    "versionar_arquivo": versionar_arquivo,
    "listar_prs": listar_prs,
    "aprovar_pr": aprovar_pr,
    "merge_pr": merge_pr,
    "versionar_arquivo_models": versionar_arquivo_models,
    "criar_branch": criar_branch,
    "criar_repositorio_gitflow": criar_repositorio_gitflow,
}
