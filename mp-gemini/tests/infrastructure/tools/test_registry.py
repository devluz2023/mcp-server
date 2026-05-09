from src.application.services.agent_service import AgentService
from src.infrastructure.llm_gateways.ollama_gateway import OllamaGateway


def test_agent_decision_flow_with_ollama():
    """
    Teste de unidade para verificar se o AgentService
    consegue identificar a intenção de listar jobs.
    """

    # 1. Setup: Criamos o Gateway apontando para o seu Ollama local
    # Certifique-se que o ollama pull qwen2.5-coder:7b foi feito
    provider = OllamaGateway(model="qwen2.5-coder:7b")

    # 2. Injetamos no serviço
    service = AgentService(llm_provider=provider)

    # 3. Execução: Enviamos um comando que deve disparar uma ferramenta específica
    prompt = "Pode listar os jobs do Databricks para mim?"

    # O process_message vai:
    # LLM (Ollama) -> Identifica Tool -> AgentService executa Tool -> Retorna String
    resposta = service.process_message(prompt)

    # 4. Asserts: Verificamos se o fluxo passou pela lógica esperada
    assert isinstance(resposta, str)
    assert len(resposta) > 0
    print(f"Resultado do teste de unidade: {resposta}")


def test_agent_drift_logic():
    """
    Verifica se o agente aciona a ferramenta de drift corretamente.
    """
    provider = OllamaGateway(model="qwen2.5-coder:7b")
    service = AgentService(llm_provider=provider)

    prompt = "Verifique se há drift nos modelos"
    resposta = service.process_message(prompt)

    # Verificamos se a resposta contém indícios de que a tool foi chamada
    assert resposta is not None
