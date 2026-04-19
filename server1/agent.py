# agent_orchestrator.py
from langchain.agents import create_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langchain_ollama import ChatOllama

# Configuração do Modelo
llm = ChatOllama(model="deepseek-r1:8b", base_url="http://localhost:11434")

# Definição das Ferramentas
@tool
def rodar_testes_docker():
    """Executa testes unitários no container de logística."""
    # Aqui você chamaria sua lógica de teste via MCP
    return "✅ Testes concluídos com sucesso via Docker!"

@tool
def analisar_logs_docker():
    """Analisa os logs do container."""
    # Aqui você chamaria sua lógica de logs via MCP
    return "🔍 Logs analisados: Sistema estável."

tools = [rodar_testes_docker, analisar_logs_docker]

# Prompt e Executor
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente de logística. Responda de forma curta e direta."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)
subagent = AgentExecutor(agent=agent, tools=tools, verbose=True)

def processar_interacao(user_input):
    return subagent.invoke({"input": user_input})