import docker
from mcp.server.fastmcp import FastMCP
import subprocess
mcp = FastMCP("LogisticaAnalyticsServer")
client = docker.from_env()
import sys
from bert_model import classificar_urgencia, classificar_resultado_teste, processar_ou_recuperar

@mcp.tool()
def get_docker_logs(container_name: str) -> str:
    """Busca logs de um container específico."""
    container = client.containers.get(container_name)
    logs = container.logs(tail=100).decode("utf-8")
    
    # Executa a classificação usando o BERT (o "porteiro" inteligente)
    urgencia = processar_ou_recuperar(logs, classificar_urgencia)
    
    # Retorna uma string formatada que o agent.py saberá interpretar
    return f"URGENCIA: {urgencia}\n\nLOGS:\n{logs}"


@mcp.tool()
def run_unit_tests() -> str:
    """Executa o comando 'pytest' e retorna o status classificado pelo BERT."""
    try:
        container = client.containers.get("logistica-sku-analytics")
        
        # Executa o pytest
        exit_code, output = container.exec_run(cmd="pytest", workdir="/app")
        resultado_log = output.decode('utf-8')
        
        # Classifica com o BERT (sempre, para ter o status do IA)
        status_ia =  processar_ou_recuperar(resultado_log, classificar_resultado_teste)
        
        # Formata o retorno de forma limpa para o agente
        cabecalho = f"--- RESULTADO IA: {status_ia} ---\n"
        corpo = f"Exit Code: {exit_code}\n\nOutput:\n{resultado_log}"
        
        return cabecalho + corpo
        
    except Exception as e:
        return f"Erro crítico ao tentar rodar testes: {str(e)}"


if __name__ == "__main__":
    mcp.run()