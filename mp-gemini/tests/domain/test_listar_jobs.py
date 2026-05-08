import pytest
from unittest.mock import MagicMock
from src.domain.entities.job import DatabricksJob
from src.domain.repositories.job_repository import JobRepositoryPort
from src.application.use_cases.listar_jobs import ListarJobs  # Exemplo de caminho

def test_listar_jobs_deve_retornar_lista_correta():
    # 1. ARRANGE (Preparação)
    # Criamos um "mock" que implementa a interface do repositório
    mock_repo = MagicMock(spec=JobRepositoryPort)
    
    # Definimos o que o mock deve retornar quando chamado
    mock_repo.list_jobs.return_value = [
        DatabricksJob(job_id=1, name="Job Teste 1"),
        DatabricksJob(job_id=2, name="Job Teste 2")
    ]
    
    # Injetamos o mock no nosso caso de uso
    use_case = ListarJobs(repository=mock_repo)
    
    # 2. ACT (Execução)
    resultado = use_case.execute()
    
    # 3. ASSERT (Verificação)
    assert len(resultado) == 2
    assert resultado[0].name == "Job Teste 1"
    mock_repo.list_jobs.assert_called_once()