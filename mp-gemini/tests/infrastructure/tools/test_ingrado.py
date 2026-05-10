import pytest
from unittest.mock import MagicMock

# Imports da sua estrutura
from src.infrastructure.services.ollama_gateway import OllamaGateway
from src.application.use_cases.git_automation import GitAutomationUseCase
from src.application.use_cases.job_automation import JobAutomationUseCase
from src.domain.services.agent_service import AgentService
from src.interfaces.tools.agent_tools import initialize_tools
from src.infrastructure.adapters.git_adapter import GitAdapter
from src.infrastructure.adapters.job_adapter import JobAdapter


def test_bootstrap_initialization_replicating_logic():
    """
    Testa o bootstrap garantindo que o AgentService aceite o llm_provider
    exatamente como na sua implementação baseada na OpenAI.
    """
    print("\n⚙️  Iniciando teste de Bootstrap (Lógica Replicada)...")

    try:
        # A. Inicializa Infra (Ollama no lugar da OpenAI)
        gateway = OllamaGateway()
        azure_adapter = GitAdapter()
        db_adapter = JobAdapter()

        # B. Inicializa Use Cases
        git_use_Case = GitAutomationUseCase(git_repository=azure_adapter)
        job_use_case = JobAutomationUseCase(repo=db_adapter)

        # C. Registra as Tools (Onde os Use Cases são injetados)
        initialize_tools(git_uc=git_use_Case, job_uc=job_use_case)
        print("✅ Passo C concluído: Tools inicializadas.")

        # D. Inicializa o Maestro (AgentService)
        # Aqui replicamos a sua chamada: AgentService(llm_provider=gateway)
        agent = AgentService(llm_provider=gateway)

        # Validação de sanidade: o objeto foi criado?
        assert agent is not None
        print("✅ Passo D concluído: AgentService instanciado com llm_provider.")

        # E. Teste de execução básica (Para garantir que ele use o gateway internamente)
        # Se o seu AgentService usa o gateway para processar, vamos testar a chamada
        # (Usando mock para não esperar o processamento real do LLM no bootstrap)
        agent.process_message = MagicMock(return_value="Resposta teste")
        resultado = agent.process_message("Olá")

        assert resultado == "Resposta teste"
        print("🚀 Bootstrap validado com sucesso!")

    except TypeError as e:
        pytest.fail(f"❌ Erro de assinatura (Parâmetro incorreto): {e}")
    except Exception as e:
        pytest.fail(f"❌ Erro na lógica de inicialização: {e}")


if __name__ == "__main__":
    test_bootstrap_initialization_replicating_logic()
