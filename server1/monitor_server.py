import docker
from mcp.server.fastmcp import FastMCP
import logging
import sys
from bert_model import classificar_urgencia, classificar_resultado_teste, processar_ou_recuperar

# Configuração do logger para visibilidade no terminal do servidor
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("LogisticaAnalyticsServer")

mcp = FastMCP("LogisticaAnalyticsServer")
client = docker.from_env()

@mcp.tool()
def get_docker_logs(container_name: str) -> str:
    """Busca logs de um container específico."""
    logger.info(f"Ferramenta 'get_docker_logs' chamada para: {container_name}")
    
    try:
        container = client.containers.get(container_name)
        logs = container.logs(tail=100).decode("utf-8")
        logger.info(f"Logs obtidos do container {container_name} ({len(logs)} bytes).")
        
        # Executa a classificação usando o BERT
        urgencia = processar_ou_recuperar(logs, classificar_urgencia)
        logger.info(f"Classificação de urgência concluída: {urgencia}")
        
        return f"URGENCIA: {urgencia}\n\nLOGS:\n{logs}"
        
    except Exception as e:
        logger.error(f"Erro ao acessar logs do container {container_name}: {str(e)}")
        return f"Erro ao obter logs: {str(e)}"

@mcp.tool()
def run_unit_tests() -> str:
    """Executa o comando 'pytest' e retorna o status classificado pelo BERT."""
    logger.info("Ferramenta 'run_unit_tests' iniciada.")
    
    try:
        container = client.containers.get("logistica-sku-analytics")
        
        logger.info("Executando 'pytest' dentro do container 'logistica-sku-analytics'...")
        exit_code, output = container.exec_run(cmd="pytest", workdir="/app")
        resultado_log = output.decode('utf-8')
        
        # Classifica com o BERT
        status_ia = processar_ou_recuperar(resultado_log, classificar_resultado_teste)
        logger.info(f"Testes finalizados. Status IA: {status_ia} | Exit Code: {exit_code}")
        
        # Formata o retorno
        cabecalho = f"--- RESULTADO IA: {status_ia} ---\n"
        corpo = f"Exit Code: {exit_code}\n\nOutput:\n{resultado_log}"
        
        return cabecalho + corpo
        
    except Exception as e:
        logger.error(f"Falha crítica na execução dos testes: {str(e)}")
        return f"Erro crítico ao tentar rodar testes: {str(e)}"

if __name__ == "__main__":
    logger.info("Iniciando servidor MCP...")
    mcp.run()