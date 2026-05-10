from abc import ABC, abstractmethod


class LLMProviderPort(ABC):
    @abstractmethod
    def invoke(self, messages: list, tools: list):
        """Interface padrão que qualquer LLM (OpenAI, Anthropic, Gemini) deve seguir."""
        pass
