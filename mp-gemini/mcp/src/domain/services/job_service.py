from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from src.domain.entities.job import Job


@dataclass
class JobExecutionResult:
    """Representa o resultado do disparo ou monitoramento de um Job"""

    success: bool
    run_id: Optional[int] = None
    error_log: Optional[str] = None


class JobService(ABC):
    @abstractmethod
    def validate_job_config(self, job: Job) -> bool:
        """Valida se as configurações do Job (cluster, path) são permitidas"""
        pass

    @abstractmethod
    def run_safe_execution(self, job: Job) -> JobExecutionResult:
        """Executa um job garantindo que não haja duplicidade ou erros críticos"""
        pass
