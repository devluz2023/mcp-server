from dataclasses import dataclass
from typing import List

# Ajustado para o seu arquivo: domain/entities/job.py
from src.domain.entities.job import Job as JobEnt
from src.domain.repositories.job_repository import JobRepository as JobRepoInterface


@dataclass
class JobAutomationUseCase:
    """
    Orquestra as operações de Job no Databricks.
    """

    job_repository: JobRepoInterface

    def execute_create_job(
        self, name: str, cluster_id: str, notebook_path: str
    ) -> JobEnt:
        # Criamos a entidade Job conforme sua definição em entities/job.py
        job = JobEnt(
            job_id=0, name=name, cluster_id=cluster_id, notebook_path=notebook_path
        )
        return self.job_repository.criar_job(job)

    def execute_list_jobs(self) -> List[JobEnt]:
        return self.job_repository.listar_jobs()

    def execute_delete_job(self, job_id: int) -> bool:
        return self.job_repository.deletar_job(job_id)
