from langchain_core.messages import HumanMessage
from src.application.ports.llm_provider import LLMProviderPort
from src.infrastructure.tools.registry import tools

class AgentService:
    def __init__(self, llm_provider: LLMProviderPort):
        self.llm_provider = llm_provider

    def process_message(self, prompt: str):
        # O serviço não sabe se é OpenAI ou outro, apenas que segue o contrato
        response = self.llm_provider.invoke([HumanMessage(content=prompt)], tools)
        
        if response.tool_calls:
            results = []
            for call in response.tool_calls:
                name = call["name"]
                if name in tools:
                    # Executa a tool do registro
                    results.append(str(tools[name].invoke(call.get("args", {}))))
            return "\n".join(results)
        return response.content