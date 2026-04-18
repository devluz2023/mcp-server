import docker
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("LogisticaAnalyticsServer")
client = docker.from_env()

@mcp.tool()
def get_docker_logs(container_name: str) -> str:
    """Busca logs de um container específico."""
    container = client.containers.get(container_name)
    return container.logs(tail=100).decode('utf-8')

if __name__ == "__main__":
    mcp.run()