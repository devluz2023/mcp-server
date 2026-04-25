from databricks.sdk import WorkspaceClient
import os
from dotenv import load_dotenv
import json
import requests
import pandas as pd
import subprocess
from databricks.sdk.service.jobs import JobSettings, Task, NotebookTask, SparkPythonTask
from pyspark.sql import functions as F
import sys
load_dotenv()
from databricks.connect import DatabricksSession
import requests
import os
import json

# =========================
# WORKSPACE CLIENT (REST API)
# =========================
w = WorkspaceClient(
    host=os.getenv("DATABRICKS_HOST"),
    token=os.getenv("DATABRICKS_TOKEN")
)

cluster_id = os.getenv("DATABRICKS_CLUSTER_ID")


# =========================
# LAZY LOAD (CORRETO)
# =========================
def get_spark():
    from databricks.connect import DatabricksSession
    return DatabricksSession.builder.getOrCreate()


def get_fe():
    # ⚠️ só funciona se Databricks Connect estiver OK
    from databricks.feature_engineering import FeatureEngineeringClient
    return FeatureEngineeringClient()


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



def criar_dashboard_padrao():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        caminho = os.path.join(
            base_dir,
            "..",
            "dashboard",
            "agent_monitoring_dashboard.lvdash.json"
        )

        with open(caminho, "r") as f:
            payload = json.load(f)

        url = f"{os.getenv('DATABRICKS_HOST')}/api/2.0/lakeview/dashboards"

        headers = {
            "Authorization": f"Bearer {os.getenv('DATABRICKS_TOKEN')}",
            "Content-Type": "application/json"
        }

        response = requests.post(url, headers=headers, json=payload)

        if response.status_code != 200:
            return f"Erro: {response.text}"

        data = response.json()

        return f"Dashboard criado! ID: {data.get('dashboard_id')}"

    except Exception as e:
        return str(e)


def listar_modelos():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    models_dir = os.path.join(base_dir, "..", "models")

    arquivos = [
        f for f in os.listdir(models_dir)
        if f.endswith(".py")
    ]

    return arquivos


def criar_job_modelo(nome_arquivo: str):
    try:
        cluster_id = os.getenv("DATABRICKS_CLUSTER_ID")

        if not cluster_id:
            return "Erro: DATABRICKS_CLUSTER_ID não configurado"

        workspace_path = f"/Shared/models/{nome_arquivo}"

        job = w.jobs.create(
            name=f"Job - {nome_arquivo}",
            tasks=[
                Task(
                    task_key="task_model",
                    existing_cluster_id=cluster_id,
                    spark_python_task=SparkPythonTask(
                        python_file=workspace_path
                    )
                )
            ]
        )

        return f"Job criado com sucesso! ID: {job.job_id}"

    except Exception as e:
        return f"Erro ao criar job: {str(e)}"

def upload_modelo(nome_arquivo: str):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        local_path = os.path.join(base_dir, "..", "models", nome_arquivo)

        workspace_folder = "/Shared/models"
        workspace_path = f"{workspace_folder}/{nome_arquivo}"

        # ✅ 1. Criar pasta se não existir
        try:
            w.workspace.mkdirs(path=workspace_folder)
        except Exception:
            pass  # se já existir, ignora

        # ✅ 2. Upload do arquivo
        w.workspace.upload(
            path=workspace_path,
            content=open(local_path, "rb"),
            overwrite=True
        )

        return workspace_path

    except Exception as e:
        return f"Erro ao subir modelo: {str(e)}"
    

def deploy_modelo(nome_arquivo: str):
    try:
        # 1. upload
        workspace_path = upload_modelo(nome_arquivo)

        if "Erro" in workspace_path:
            return workspace_path

        # 2. criar job
        result = criar_job_modelo(nome_arquivo)

        return f"""
        ✅ Modelo enviado: {workspace_path}
        🚀 {result}
        """

    except Exception as e:
        return str(e)
    
def executar_pipeline_fixo():

    """
    Lê CSV local e grava no Databricks como tabela Delta.
    """

    try:
        # =========================
        # Spark session
        # =========================
        spark = DatabricksSession.builder.getOrCreate()

        # =========================
        # Config fixo
        # =========================
        CATALOGO = "pedido"
        SCHEMA = "default"
        TABELA = "cliente"

        FULL_TABLE_NAME = f"{CATALOGO}.{SCHEMA}.{TABELA}"

        # =========================
        # Criar schema
        # =========================
        spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOGO}.{SCHEMA}")

        # =========================
        # CSV fixo
        # =========================
        local_csv_path = (
            "/Users/fabiojuliodaluz/Documents/GitHub/mcp-server/"
            "arquitetura_de_dados/data/BancoDeDados.csv"
        )

        if not os.path.exists(local_csv_path):
            return f"Arquivo não encontrado: {local_csv_path}"

        # =========================
        # Ler CSV
        # =========================
        df_pd = pd.read_csv(local_csv_path)
        df_spark = spark.createDataFrame(df_pd)

        # =========================
        # Escrever Delta Table
        # =========================
        df_spark.write \
            .format("delta") \
            .mode("overwrite") \
            .option("overwriteSchema", "true") \
            .saveAsTable(FULL_TABLE_NAME)

        return f"✔ Carga concluída com sucesso: {FULL_TABLE_NAME}"

    except Exception as e:
        return f"Erro na carga: {str(e)}"