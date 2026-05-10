from databricks.sdk import WorkspaceClient
from src.domain.entities.job import Job
from src.domain.repositories.job_repository import JobRepository as JobInterface
from config import settings


class JobAdapter(JobInterface):
    def __init__(self):
        self.client = WorkspaceClient(
            host=settings.DATABRICKS_HOST, token=settings.DATABRICKS_TOKEN
        )

    def criar_job(self, job: Job) -> Job:
        created_job = self.client.jobs.create(
            name=job.name,
            tasks=[
                {
                    "task_key": job.task_key,
                    "existing_cluster_id": settings.DATABRICKS_CLUSTER_ID,
                    "notebook_task": {"notebook_path": job.notebook_path},
                }
            ],
        )
        job.job_id = created_job.job_id
        return job

    def listar_jobs(self) -> list[Job]:
        jobs_sdk = self.client.jobs.list()
        return [Job(job_id=j.job_id, name=j.settings.name) for j in jobs_sdk]

    def deletar_job(self, job_id: int) -> bool:
        self.client.jobs.delete(job_id=job_id)
        return True

    # --- ADICIONE ESTE MÉTODO ---
    def executar_job(self, job_id: int) -> bool:
        print(f"Executando Job {job_id} no Databricks")
        self.client.jobs.run_now(job_id=job_id)
        return True
