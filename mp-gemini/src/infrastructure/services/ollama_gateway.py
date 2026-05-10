from langchain_ollama import ChatOllama
from src.domain.repositories.llm_provider import LLMProviderPort


class OllamaGateway(LLMProviderPort):
    def __init__(self, model="qwen2.5-coder:7b"):
        # Centralizamos a configuração aqui.
        # O base_url aponta para o seu Ollama local no Mac.
        self.llm = ChatOllama(
            model=model, temperature=0, base_url="http://localhost:11434"
        )

    def invoke(self, messages, tools):
        """
        Faz o bind das ferramentas e invoca o modelo.
        """
        # Garante que as tools estejam em formato de lista para o LangChain
        list_of_tools = list(tools.values()) if isinstance(tools, dict) else tools

        # O bind_tools prepara o LLM para decidir qual função chamar
        llm_with_tools = self.llm.bind_tools(list_of_tools)
        return llm_with_tools.invoke(messages)
