import pytest
from src.interfaces.tools.agent_tools import initialize_tools, get_tools
from unittest.mock import MagicMock

def test_initialize_tools_registers_correctly():
    """
    Testa se as ferramentas são registradas no dicionário global.
    """
    # Criamos Mocks para não precisar de conexão real com Azure/Databricks no teste
    mock_git_uc = MagicMock()
    mock_job_uc = MagicMock()

    # Executa a inicialização
    initialize_tools(mock_git_uc, mock_job_uc)
    
    # Obtém o registro
    tools_dict = get_tools()

    # Asserts (O que o pytest valida)
    assert len(tools_dict) > 0
    assert "criar_branch_ml" in tools_dict
    assert "listar_jobs_databricks" in tools_dict
    print("\n✅ Teste de registro de ferramentas passou!")

def test_get_tools_returns_dict():
    """
    Garante que o get_tools retorna um dicionário (para evitar o erro anterior).
    """
    tools = get_tools()
    assert isinstance(tools, dict)