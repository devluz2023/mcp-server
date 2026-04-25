from databricks.sdk import WorkspaceClient
import os
from dotenv import load_dotenv
load_dotenv()
from databricks.sdk.service.jobs import JobSettings
from databricks.sdk.service.jobs import Task, NotebookTask
# Inicializa o cliente uma única vez. 
# Ele lerá automaticamente as variáveis DATABRICKS_HOST e DATABRICKS_TOKEN do seu ambiente.
w = WorkspaceClient(
    host=os.getenv("DATABRICKS_HOST"),
    token=os.getenv("DATABRICKS_TOKEN")
)

cluster_id = os.getenv("DATABRICKS_CLUSTER_ID")

# =========================
# LISTAR JOBS
# =========================
def listar_jobs():
    """Lista todos os jobs disponíveis."""
    try:
        lista = []

        for j in w.jobs.list():
            nome = j.settings.name if j.settings else "Sem nome"
            lista.append(f"ID: {j.job_id} | Nome: {nome}")

        return "\n".join(lista) if lista else "Nenhum job encontrado."

    except Exception as e:
        return f"Erro ao listar jobs: {str(e)}"


# =========================
# EXECUTAR JOB
# =========================
def executar_job(job_id: int):
    """Executa um job pelo ID."""
    try:
        run = w.jobs.run_now(job_id=job_id)
        return f"Job {job_id} iniciado com sucesso. Run ID: {run.run_id}"

    except Exception as e:
        return f"Erro ao executar job: {str(e)}"


# =========================
# CRIAR JOB
# =========================
def criar_job(nome: str):
    """Cria um job simples no Databricks."""
    try:
        cluster_id = os.getenv("DATABRICKS_CLUSTER_ID")

        if not cluster_id:
            return "Erro: DATABRICKS_CLUSTER_ID não configurado."

        job = w.jobs.create(
            name=nome,
            tasks=[
                Task(
                    task_key="task-1",
                    existing_cluster_id=cluster_id,
                    notebook_task=NotebookTask(
                        notebook_path="/Workspace/Users/seu_usuario/exemplo_notebook"
                    )
                )
            ]
        )

        return f"Job criado com sucesso! ID: {job.job_id}"

    except Exception as e:
        return f"Erro ao criar job: {str(e)}"

# =========================
# ATUALIZAR JOB
# =========================

def atualizar_job(job_id: int, novo_nome: str):
    """Atualiza o nome de um job."""
    try:
        w.jobs.update(
            job_id=job_id,
            new_settings=JobSettings(
                name=novo_nome
            )
        )

        return f"Job {job_id} atualizado para '{novo_nome}'"

    except Exception as e:
        return f"Erro ao atualizar job: {str(e)}"

# =========================
# DELETAR JOB
# =========================
def deletar_job(job_id: int):
    """Remove um job pelo ID."""
    try:
        w.jobs.delete(job_id=job_id)
        return f"Job {job_id} deletado com sucesso."

    except Exception as e:
        return f"Erro ao deletar job: {str(e)}"
    

def calcular_custo(run_id: int):
    """Consulta o custo via System Tables."""
    query = f"""
        SELECT SUM(usage_quantity * list_prices.pricing.default) as custo_estimado
        FROM system.billing.usage
        WHERE usage_metadata.job_run_id = '{run_id}'
        """

    response = w.statement_execution.execute_statement(
        statement=query,
        warehouse_id=os.getenv("DATABRICKS_WAREHOUSE_ID")  # ⚠️ obrigatório
    )

    # 🔥 pegar resultado
    if response.result and response.result.data_array:
        custo = float(response.result.data_array[0][0])
        return f"Custo estimado para o Run {run_id}: ${custo:.4f}"

    return "Custo não disponível ou Run ID inválido."