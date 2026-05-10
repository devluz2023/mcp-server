from dataclasses import dataclass

# Ajustado para o seu arquivo: domain/entities/job.py
from src.domain.repositories.job_repository import JobRepository as JobRepoInterface


@dataclass
class JobAutomationUseCase:
    """
    Orquestra as operações de Job no Databricks.
    """

    repo: JobRepoInterface

    def criar_job(self, nome: str) -> str:
        return self.repo.criar_job(nome)

    def listar_jobs(self) -> str:
        return self.repo.listar_jobs()

    def deletar_job(self, job_id: int) -> bool:
        return self.repo.deletar_job(job_id)

    def executar_job(self, job_id: int) -> bool:
        return self.repo.executar_job(job_id)

    def atualizar_job(self, job_id: int, novo_nome: str) -> str:
        return self.repo.atualizar_job(job_id, novo_nome)

    def calcular_custo(self, run_id: int) -> str:
        return self.repo.calcular_custo(run_id)

    def criar_dashboard_padrao(self) -> str:
        return self.repo.criar_dashboard_padrao()

    def listar_modelos(self) -> str:
        return self.repo.listar_modelos()

    def upload_modelo(self, nome_arquivo: str) -> str:
        return self.repo.upload_modelo(nome_arquivo)

    def deploy_modelo(self, nome_arquivo: str) -> str:
        return self.repo.deploy_modelo(nome_arquivo)

    def bundle_job_yaml(self) -> str:
        return self.repo.bundle_job_yaml()

    def executar_pipeline_csv_para_feature_store(self) -> str:
        return self.repo.executar_pipeline_csv_para_feature_store()

    def show_drift(self) -> str:
        return self.repo.show_drift()
