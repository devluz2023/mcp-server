import asyncio
import operator
import logging
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from midleware import fetch_log_and_diagnose, run_tests_async

# Configuração de Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AgentGraph")

class OllamaSingleton:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            logger.info("Inicializando modelo (Singleton)...")
            cls._instance = ChatOllama(model="llama3.2", base_url="http://ollama:11434")
        return cls._instance

def get_llm():
    return OllamaSingleton()

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    master_decision: str

llm = get_llm()

def master_node(state: AgentState):
    user_input = state['messages'][-1].content
    decision = "monitor1" if "teste" in user_input.lower() else "monitor2"
    logger.info(f"Master Node decidiu encaminhar para: {decision} (Input: '{user_input[:30]}...')")
    return {"master_decision": decision}

def monitor1_node(state: AgentState):
    logger.info("Monitor1: Iniciando execução de testes...")
    
    # Executa o serviço MCP
    result = asyncio.run(run_tests_async("logistica-sku-analytics"))
    logger.info("Monitor1: Testes concluídos via MCP.")
    
    msg_resultado = SystemMessage(content=f"RESULTADO DO TESTE: {result.content[0].text}")
    
    logger.info("Monitor1: Enviando dados para o LLM processar...")
    res = llm.invoke(state['messages'] + [msg_resultado])
    
    return {"messages": [res]}

def monitor2_node(state: AgentState):
    logger.info("Monitor2: Coletando logs de container...")
    
    logs, diag = asyncio.run(fetch_log_and_diagnose("logistica-sku-analytics"))
    logger.info(f"Monitor2: Logs recuperados. Diagnóstico RAG: {diag}")
    
    res = llm.invoke([SystemMessage(content=f"Logs: {logs[:500]}")] + state['messages'])
    return {"messages": [res]}

# Configuração do Grafo
builder = StateGraph(AgentState)
builder.add_node("master", master_node)
builder.add_node("monitor1", monitor1_node)
builder.add_node("monitor2", monitor2_node)
builder.set_entry_point("master")
builder.add_conditional_edges("master", lambda s: s["master_decision"], {"monitor1": "monitor1", "monitor2": "monitor2"})
builder.add_edge("monitor1", END)
builder.add_edge("monitor2", END)
graph = builder.compile()

def iterar(texto: str):
    logger.info(f"Iniciando nova iteração com o agente: {texto}")
    resultado = graph.invoke({"messages": [HumanMessage(content=texto)]})
    logger.info("Iteração finalizada com sucesso.")
    return {"decisao": resultado["master_decision"], "resposta": resultado["messages"][-1].content}