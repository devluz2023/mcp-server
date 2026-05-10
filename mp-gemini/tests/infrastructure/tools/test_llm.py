import pytest
from src.infrastructure.services.ollama_gateway import OllamaGateway
from langchain_core.messages import HumanMessage


def test_ollama_connection_and_invoke():
    """
    Testa a conexão direta com o Ollama sem envolver ferramentas ou serviços complexos.
    """
    print("\n📡 Testando conexão direta com Ollama...")

    # 1. Inicializa o Gateway (usando o parâmetro 'model' que confirmamos antes)
    try:
        # Usando o qwen2.5-coder que você já tem configurado
        gateway = OllamaGateway(model="qwen2.5-coder:7b")
    except Exception as e:
        pytest.fail(f"Falha ao instanciar o OllamaGateway: {e}")

    # 2. Prepara uma mensagem simples
    messages = [HumanMessage(content="Diga 'Conexão OK' se estiver me ouvindo.")]

    # 3. Tenta invocar o modelo (passando lista vazia de tools para este teste simples)
    try:
        print("🧠 Enviando prompt para o modelo...")
        # Note que passamos tools=[] pois o seu invoke espera esse argumento
        response = gateway.invoke(messages, tools=[])

        print(f"✨ Resposta do Ollama: {response.content}")

        # Validação
        assert response.content is not None
        assert len(response.content) > 0
        print("✅ Conexão e invocação bem-sucedidas!")

    except Exception as e:
        pytest.fail(
            f"Erro na comunicação com o Ollama: {e}. O 'ollama serve' está rodando?"
        )


if __name__ == "__main__":
    test_ollama_connection_and_invoke()
