# src/infrastructure/llm_gateways/ollama_gateway.py
from langchain_ollama import ChatOllama
from src.domain.repositories.llm_provider import LLMProviderPort


class OllamaGateway(LLMProviderPort):  # Verifique se o nome está idêntico aqui
    def __init__(self, model="qwen2.5-coder:7b"):
        self.llm = ChatOllama(
            model=model, temperature=0, base_url="http://localhost:11434"
        )

    def invoke(self, messages, tools):
        # Conversão de dicionário para lista se necessário
        list_of_tools = list(tools.values()) if isinstance(tools, dict) else tools
        llm_with_tools = self.llm.bind_tools(list_of_tools)
        return llm_with_tools.invoke(messages)
