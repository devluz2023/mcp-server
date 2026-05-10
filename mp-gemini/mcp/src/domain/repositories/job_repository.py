from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.job import Job


class JobRepository(ABC):
    """
    Interface de Domínio para operações no Databricks.
    """

    @abstractmethod
    def criar_job(self, job: Job) -> Job:
        """Recebe a Entidade Job, persiste no Databricks e retorna com ID preenchido."""
        pass

    @abstractmethod
    def listar_jobs(self) -> List[Job]:
        """Recupera a lista de todos os Jobs como Entidades de Domínio."""
        pass

    @abstractmethod
    def deletar_job(self, job_id: int) -> bool:
        """Remove o job do workspace através do ID."""
        pass

    @abstractmethod
    def executar_job(self, job_id: int) -> bool:
        """Dispara a execução imediata de um job."""
        pass
