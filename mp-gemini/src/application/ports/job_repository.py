from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.job import DatabricksJob # Criaremos essa classe a seguir

class JobRepositoryPort(ABC):
    @abstractmethod
    def list_jobs(self) -> List[DatabricksJob]:
        pass

    @abstractmethod
    def delete_job(self, job_id: int) -> bool:
        pass