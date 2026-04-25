from databricks.sdk import WorkspaceClient
import os
# Inicializa o cliente uma única vez. 
# Ele lerá automaticamente as variáveis DATABRICKS_HOST e DATABRICKS_TOKEN do seu ambiente.
w = WorkspaceClient(
    host=os.getenv("DATABRICKS_HOST"),
    token=os.getenv("DATABRICKS_TOKEN")
)

def listar_jobs():
    """Busca e formata a lista de jobs."""
    try:
        jobs = w.jobs.list(limit=20)
        lista = [f"ID: {j.job_id} | Nome: {j.settings.name}" for j in jobs]
        return "\n".join(lista) if lista else "Nenhum job encontrado."
    except Exception as e:
        return f"Erro ao listar jobs: {str(e)}"

def executar_job(job_id: int):
    """Dispara a execução de um job."""
    try:
        run = w.jobs.run_now(job_id=job_id)
        return f"Job {job_id} iniciado com sucesso. Run ID: {run.run_id}"
    except Exception as e:
        return f"Erro ao executar job: {str(e)}"

def calcular_custo(run_id: int):
    """Consulta o custo via System Tables."""
    query = f"""
    SELECT SUM(usage_quantity * list_prices.pricing.default) as custo_estimado
    FROM system.billing.usage
    WHERE usage_metadata.job_run_id = '{run_id}'
    """
    try:
        # Executa a query no SQL Warehouse ou Cluster disponível
        results = w.query_history.query(query)
        if results.rows:
            custo = results.rows[0][0]
            return f"Custo estimado para o Run {run_id}: ${custo:.4f}"
        return "Custo não disponível ou Run ID inválido."
    except Exception as e:
        return f"Erro ao calcular custo: {str(e)}"