from langchain_core.tools import tool
from src.infrastructure.repositories.databricks_job_repository import DatabricksJobRepository
import os

db = DatabricksJobRepository()

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

    return "\n".join([
        f for f in os.listdir(models_dir)
        if f.endswith(".py")
    ])


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
    "pipeline_databricks":pipeline_databricks,
    "bundle_job_yaml": bundle_job_yaml,
    "show_drift": show_drift
}