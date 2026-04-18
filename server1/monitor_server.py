import docker
from mcp.server.fastmcp import FastMCP
import subprocess
mcp = FastMCP("LogisticaAnalyticsServer")
client = docker.from_env()

@mcp.tool()
def get_docker_logs(container_name: str) -> str:
    """Busca logs de um container específico."""
    container = client.containers.get(container_name)
    return container.logs(tail=100).decode('utf-8')


@mcp.tool()
def run_unit_tests(service_path: str) -> str:
    """Executa testes unitários no diretório especificado."""
    try:
        # Executa o pytest e captura o output
        result = subprocess.run(
            ["pytest", service_path], 
            capture_output=True, 
            text=True
        )
        return result.stdout + result.stderr
    except Exception as e:
        return f"Erro ao executar testes: {str(e)}"
    
if __name__ == "__main__":
    mcp.run()