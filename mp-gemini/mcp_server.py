from mcp.server.fastmcp import FastMCP
import logging
import sys
import databricks_ops as db  # O seu único arquivo de lógica

# Configuração de log para visibilidade no seu terminal
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger("LogisticaAnalyticsServer")

mcp = FastMCP("LogisticaAnalyticsServer")


@mcp.tool()
def criar_dashboard_databricks() -> str:
    """Cria um dashboard no Databricks a partir de um JSON."""
    return db.criar_dashboard_padrao()

@mcp.tool()
def listar_jobs_databricks() -> str:
    """Lista os jobs disponíveis no Databricks."""
    logger.info("Ferramenta 'listar_jobs_databricks' chamada.")
    return db.listar_jobs()

@mcp.tool()
def executar_job_databricks(job_id: int) -> str:
    """Executa um job do Databricks pelo ID."""
    logger.info(f"Executando job ID: {job_id}")
    return db.executar_job(job_id)

@mcp.tool()
def verificar_custo_job(run_id: int) -> str:
    """Consulta o custo de uma execução (run) específica."""
    logger.info(f"Consultando custo para o run: {run_id}")
    return db.calcular_custo(run_id)



@mcp.tool()
def deploy_modelo_databricks(nome_modelo: str) -> str:
    """
    Faz deploy de um modelo Python da pasta models no Databricks.
    """
    return db.deploy_modelo(nome_modelo)




@mcp.tool()
def bundle_job_yaml() -> str:
    """Cria bundle yaml"""
    return db.bundle_job_yaml



@mcp.tool()
def pipeline_databricks(nome_arquivo: str, tabela: str, feature_table: str) -> str:
    """
    Pipeline completo: CSV → Delta → Feature Store
    """
    return db.pipeline_csv_para_feature_store(nome_arquivo, tabela, feature_table)

if __name__ == "__main__":
    logger.info("Iniciando servidor MCP...")
    mcp.run()