import operator
import logging
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, END
from langchain_ollama import ChatOllama
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage
from midleware import sync_fetch_log, sync_run_tests

logger = logging.getLogger("AgentGraph")

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    master_decision: str

# USANDO MODELO LEVE PARA DESTRAVAR O MACBOOK
llm = ChatOllama(model="tinyllama", base_url="http://ollama:11434", request_timeout=60.0)

def monitor1_node(state: AgentState):
    logger.info("Monitor1: Iniciando execução de testes...")
    
    try:
        # Executa a coroutine corretamente
        result = sync_run_tests("logistica-sku-analytics")
        logger.info("Monitor1: Testes concluídos via MCP.")
        
        # Validação de segurança: Verifica se result possui conteúdo
        if result and hasattr(result, 'content') and len(result.content) > 0:
            content_text = result.content[0].text
        else:
            content_text = "Nenhum resultado retornado pelo servidor de testes."
            
        # Define a instrução do sistema
        system_instruction = SystemMessage(content="""
        Você é um engenheiro de dados especialista em logística. 
        Analise os resultados dos testes automatizados abaixo. Se houver falhas, 
        identifique a causa provável e sugira uma correção técnica.
        Se o usuário perguntar sobre algo fora do contexto, diga: 
        'Não encontrei referências a [termo] nos resultados dos testes'.
        """)
        
        # Cria a mensagem com os dados processados
        msg_resultado = SystemMessage(content=f"RESULTADO DO TESTE: {content_text[:500]}")
        
        logger.info("Monitor1: Enviando resultados para o LLM processar...")
        
        # Invoca o LLM
        # res = llm.invoke([system_instruction, msg_resultado] + state['messages'])
        
        # return {"messages": [res]}
        return content_text[:500]

    except Exception as e:
        logger.error(f"Erro crítico no Monitor1: {str(e)}")
        error_msg = SystemMessage(content=f"Erro ao processar testes: {str(e)}")
        return {"messages": [error_msg]}

def monitor2_node(state: AgentState):
    logs, diag = sync_fetch_log("logistica-sku-analytics")
    res = llm.invoke([SystemMessage(content=f"Logs: {logs[:500]}")] + state['messages'])
    return {"messages": [res]}

# COMPILAÇÃO GLOBAL (Evita reprocessamento)
builder = StateGraph(AgentState)
builder.add_node("monitor1", monitor1_node)
builder.add_node("monitor2", monitor2_node)
builder.set_entry_point("monitor2")
builder.add_edge("monitor2", END)
graph = builder.compile()

def executar_agente(texto: str):
    resultado = graph.invoke({"messages": [HumanMessage(content=texto)]})
    return {"decisao": "monitor2", "resposta": resultado["messages"][-1].content}