from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama

# 1. Definição do LLM
llm = ChatOllama(
    model="qwen2.5:1.5b",
    base_url="http://localhost:11434"
)

# 2. Definição explícita de ferramentas (Lista vazia para evitar erro)
tools = [] 

# 3. Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "Você é um assistente de logística."),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 4. Agente e Executor
agent = create_tool_calling_agent(llm, tools, prompt)
subagent = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 5. Execução
if __name__ == "__main__":
    try:
        resultado = subagent.invoke({"input": "Olá, teste de funcionamento"})
        print(resultado["output"])
    except Exception as e:
        print(f"Erro ao executar: {e}")