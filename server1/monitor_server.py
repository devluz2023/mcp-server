import docker
from mcp.server.fastmcp import FastMCP
import subprocess
mcp = FastMCP("LogisticaAnalyticsServer")
client = docker.from_env()
import sys


@mcp.tool()
def get_docker_logs(container_name: str) -> str:
    """Busca logs de um container específico."""
    container = client.containers.get(container_name)
    return container.logs(tail=100).decode('utf-8')

@mcp.tool()
def run_unit_tests() -> str:
    """
    Executa o comando 'pytest' dentro do container logistica-sku-analytics na pasta /app.
    """
    try:
        # Pega a referência do container fixo
        container = client.containers.get("logistica-sku-analytics")
        
        # Executa o pytest dentro do workdir /app
        # O comando é executado pelo shell do container
        exit_code, output = container.exec_run(
            cmd="pytest",
            workdir="/app"
        )
        
        # Decodifica a saída
        resultado = output.decode('utf-8')
        
        if exit_code != 0:
            return f"Os testes falharam (Código {exit_code}):\n{resultado}"
            
        return f"Testes concluídos com sucesso:\n{resultado}"
        
    except Exception as e:
        return f"Erro ao tentar rodar testes no container: {str(e)}"
if __name__ == "__main__":
    mcp.run()