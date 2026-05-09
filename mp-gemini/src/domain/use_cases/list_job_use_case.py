from typing import List

from src.domain.entities.job import DatabricksJob
from src.domain.repositories.job_repository import JobRepositoryPort


class ListJobsUseCase:
    def __init__(self, repository: JobRepositoryPort):
        # O Use Case só conhece o contrato, não a implementação real (Databricks)
        self.repository = repository

    def execute(self) -> List[DatabricksJob]:
        """
        Executa a regra de negócio para listar jobs.
        Aqui você poderia adicionar filtros, ordenação ou logs.
        """
        try:
            # Chama o repositório através da porta (interface)
            jobs = self.repository.list_jobs()

            # Exemplo de regra de negócio:
            # Garantir que jobs vazios sejam filtrados antes de chegar na UI
            return [j for j in jobs if j.name != "Sem nome"]

        except Exception as e:
            # O Use Case gerencia o erro de negócio, não o erro técnico da API
            raise Exception(f"Erro ao processar caso de uso de listagem: {str(e)}")
