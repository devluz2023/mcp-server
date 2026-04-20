import streamlit as st
import asyncio
import logging
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from rag_engine import analisar_log

# Configuração básica do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def fetch_log_and_diagnose(container_name):
    logger.info(f"Iniciando diagnóstico para o container: {container_name}")
    
    server_params = StdioServerParameters(command="python", args=["monitor_server.py"])
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                logger.debug("Sessão MCP inicializada com sucesso.")
                
                logger.info(f"Chamando ferramenta get_docker_logs para {container_name}...")
                log_result = await session.call_tool("get_docker_logs", {"container_name": container_name})
                
                log_text = log_result.content[0].text
                logger.info(f"Logs obtidos com sucesso. Tamanho: {len(log_text)} caracteres.")
                
                logger.info("Executando análise via RAG...")
                diagnostico = analisar_log(log_text)
                
                logger.info("Diagnóstico concluído.")
                return log_text, diagnostico
                
    except Exception as e:
        logger.error(f"Erro ao capturar logs do container {container_name}: {str(e)}", exc_info=True)
        return None, f"Erro ao processar logs: {str(e)}"

async def run_tests_async(service_path):
    logger.info(f"Executando testes unitários em: {service_path}")
    
    server_params = StdioServerParameters(command="python", args=["monitor_server.py"])
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool("run_unit_tests", {"service_path": service_path})
                logger.info(f"Testes finalizados para {service_path}.")
                return result
                
    except Exception as e:
        logger.error(f"Falha ao executar testes unitários: {str(e)}", exc_info=True)
        raise e