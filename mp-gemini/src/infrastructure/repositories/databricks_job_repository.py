import logging
import os
from typing import List

from databricks.sdk import WorkspaceClient
from src.application.ports.job_repository import JobRepositoryPort
from src.domain.entities.job import DatabricksJob
from dotenv import find_dotenv, load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(find_dotenv())

# Configura um logger para avisar que algo falhou sem travar o app
logger = logging.getLogger(__name__)


class DatabricksJobRepository(JobRepositoryPort):
    def __init__(self):
        # Apenas guardamos a configuração, não instanciamos o cliente ainda
        self.host = os.getenv("DATABRICKS_HOST")
        self.token = os.getenv("DATABRICKS_TOKEN")
        self._client = None

    @property
    def client(self):
        """Getter que cria o cliente apenas quando necessário."""
        if self._client is None:
            if not self.host or not self.token:
                logger.warning("Credenciais do Databricks não encontradas!")
                raise ConnectionError("DATABRICKS_HOST ou TOKEN não configurados.")

            try:
                self._client = WorkspaceClient(host=self.host, token=self.token)
            except Exception as e:
                logger.error(f"Erro ao inicializar cliente Databricks: {e}")
                raise
        return self._client

    # No seu DatabricksJobRepository
    def list_jobs(self) -> List[DatabricksJob]:
        sdk_jobs = self.client.jobs.list()
        # Tradução: SDK -> Entidade de Domínio
        return [DatabricksJob(job_id=j.job_id, name=j.settings.name) for j in sdk_jobs]

    def delete_job(self, job_id: int) -> bool:
        try:
            self.client.jobs.delete(job_id=job_id)
            return True
        except Exception as e:
            logger.error(f"Falha ao deletar job {job_id}: {e}")
            return False
