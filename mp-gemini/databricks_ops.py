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
import yaml
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
from databricks.sdk.service.workspace import ImportFormat


def upload_modelo(nome_arquivo: str):
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        local_path = os.path.join(base_dir, "..", "models", nome_arquivo)

        workspace_folder = "/Users/fabio.jdluz@gmail.com/models" # Criei uma pasta models dentro do seu usuário para organizar
        workspace_path = f"{workspace_folder}/{nome_arquivo}"

        # 1. Cria a pasta
        w.workspace.mkdirs(path=workspace_folder)

        # 2. Upload com formato FORÇADO para SOURCE (Script Python)
        with open(local_path, "rb") as f:
            w.workspace.upload(
                path=workspace_path,
                content=f,
                overwrite=True,
                 format=ImportFormat.AUTO # Isso diz ao Databricks: "trate como código fonte"
            )

        return workspace_path

    except Exception as e:
        return f"Erro ao subir modelo: {str(e)}"

    except Exception as e:
        return f"Erro ao subir modelo: {str(e)}"

def criar_job_modelo(nome_arquivo: str, workspace_path: str):
    cluster_id = os.getenv("DATABRICKS_CLUSTER_ID")

    # O Spark entende caminhos absolutos do Workspace corretamente aqui
    job = w.jobs.create(
        name=f"Job - {nome_arquivo}",
        tasks=[
            Task(
                task_key="model",
                existing_cluster_id=cluster_id,
                spark_python_task=SparkPythonTask(
                    python_file=workspace_path
                )
            )
        ]
    )
    return job.job_id

def deploy_modelo(nome_arquivo: str):
    try:
        workspace_path = upload_modelo(nome_arquivo)
        
        if isinstance(workspace_path, str) and "Erro" in workspace_path:
            return workspace_path

        job_id = criar_job_modelo(nome_arquivo, workspace_path)

        return f"✅ Modelo enviado para: {workspace_path}\n🚀 Job criado! ID: {job_id}"

    except Exception as e:
        return f"Erro no deploy: {str(e)}"



def bundle_job_yaml():

    """
    Lê YAML fixo e cria Job no Databricks usando SDK tipado corretamente.
    """

    import os
    import yaml
    from dotenv import load_dotenv
    from databricks.sdk import WorkspaceClient
    from databricks.sdk.service.jobs import Task, SparkPythonTask

    load_dotenv()

    w = WorkspaceClient(
        host=os.getenv("DATABRICKS_HOST"),
        token=os.getenv("DATABRICKS_TOKEN")
    )

    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))

        yaml_path = os.path.join(
            base_dir,
            "..",
            "models",
            "job_model.yaml"
        )

        if not os.path.exists(yaml_path):
            return f"❌ YAML não encontrado: {yaml_path}"

        with open(yaml_path, "r") as f:
            config = yaml.safe_load(f)

        job_cfg = list(config["resources"]["jobs"].values())[0]
        task_cfg = job_cfg["tasks"][0]

        # =========================
        # SDK TIPADO (CORRETO)
        # =========================
        task = Task(
            task_key=task_cfg["task_key"],
            existing_cluster_id=task_cfg["existing_cluster_id"],
            spark_python_task=SparkPythonTask(
                python_file=task_cfg["spark_python_task"]["python_file"]
            )
        )

        response = w.jobs.create(
            name=job_cfg["name"],
            tasks=[task]
        )

        return {
            "status": "success",
            "job_id": response.job_id,
            "job_name": job_cfg["name"]
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


import os
import pandas as pd
from pyspark.sql import functions as F

def executar_pipeline_csv_para_feature_store():
    """
    Pipeline fixo:
    CSV local → Spark DataFrame → Delta Table → Feature Store (ou fallback Delta)
    """

    try:
        # =========================
        # Spark session
        # =========================
        from databricks.connect import DatabricksSession
        from databricks.feature_engineering import FeatureEngineeringClient

        spark = DatabricksSession.builder.getOrCreate()

        try:
            fe = FeatureEngineeringClient()
        except:
            fe = None  # fallback se Feature Store não estiver disponível

        # =========================
        # CONFIG FIXA
        # =========================
        catalog = "pedido"
        schema = "default"
        table = "cliente"
        feature_table = "cliente_features"

        base_table = f"{catalog}.{schema}.{table}"
        feature_table_name = f"{catalog}.{schema}.{feature_table}"

        # =========================
        # CSV FIXO
        # =========================
        csv_path = (
            "/Users/fabiojuliodaluz/Documents/GitHub/mcp-server/"
            "arquitetura_de_dados/data/BancoDeDados.csv"
        )

        if not os.path.exists(csv_path):
            return f"CSV não encontrado: {csv_path}"

        # =========================
        # LOAD CSV
        # =========================
        df_pd = pd.read_csv(csv_path)
        df = spark.createDataFrame(df_pd)

        # =========================
        # CRIA SCHEMA
        # =========================
        spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{schema}")

        # =========================
        # SALVA TABELA BASE
        # =========================
        df.write.format("delta").mode("overwrite").saveAsTable(base_table)

        # =========================
        # FEATURES
        # =========================
        df_features = df.groupBy("id_unico_cliente").agg(
            F.count("*").alias("total_registros"),
            F.avg("preco").alias("ticket_medio"),
            F.sum("preco").alias("valor_total")
        )

        # =========================
        # FEATURE STORE (ou fallback)
        # =========================
        if fe:
            try:
                fe.create_table(
                    name=feature_table_name,
                    primary_keys=["id_unico_cliente"],
                    df=df_features
                )
            except:
                df_features.write.format("delta").mode("overwrite").saveAsTable(feature_table_name)
        else:
            df_features.write.format("delta").mode("overwrite").saveAsTable(feature_table_name)

        return {
            "status": "success",
            "base_table": base_table,
            "feature_table": feature_table_name
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }