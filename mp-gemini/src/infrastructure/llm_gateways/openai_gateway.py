from langchain_openai import ChatOpenAI
from src.application.ports.llm_provider import LLMProviderPort

class OpenAIGateway(LLMProviderPort):
 
    def __init__(self, api_key: str, model="gpt-4o-mini"):
        if not api_key:
            raise ValueError("API Key é obrigatória para o OpenAIGateway")
        self.llm = ChatOpenAI(model=model, temperature=0, api_key=api_key)

    def invoke(self, messages, tools):
        llm_with_tools = self.llm.bind_tools(list(tools.values()))
        return llm_with_tools.invoke(messages)