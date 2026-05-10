from databricks.sdk import WorkspaceClient
from src.domain.repositories.job_repository import JobRepository as JobInterface
from config import settings
from databricks.sdk.service.jobs import JobSettings, NotebookTask, SparkPythonTask, Task
import os
import yaml
import json
from databricks.sdk.service.workspace import ImportFormat
import requests
from databricks.connect import DatabricksSession
import pandas as pd
from pyspark.sql import functions as F
import numpy as np
from scipy.stats import chi2_contingency, ks_2samp


class JobAdapter(JobInterface):
    def __init__(self):
        self.worskpace = WorkspaceClient(
            host=settings.DATABRICKS_HOST, token=settings.DATABRICKS_TOKEN
        )
        self.cluster_id = settings.DATABRICKS_CLUSTER_ID
        self.warehouse_id = settings.DATABRICKS_WAREHOUSE_ID

    def criar_job(self, nome: str) -> str:
        if not self.cluster_id:
            return "Erro: DATABRICKS_CLUSTER_ID não configurado."

        job = self.worskpace.jobs.create(
            name=nome,
            tasks=[
                Task(
                    task_key="task-1",
                    existing_cluster_id=self.cluster_id,
                    notebook_task=NotebookTask(
                        notebook_path="/Workspace/Users/seu_usuario/exemplo_notebook"
                    ),
                )
            ],
        )

        return f"Job criado com sucesso! ID: {job.job_id}"

    def listar_jobs(self) -> str:
        """Lista todos os jobs disponíveis."""
        w = self.worskpace
        try:
            lista = []

            for j in w.jobs.list():
                nome = j.settings.name if j.settings else "Sem nome"
                lista.append(f"ID: {j.job_id} | Nome: {nome}")

            return "\n".join(lista) if lista else "Nenhum job encontrado."

        except Exception as e:
            return f"Erro ao listar jobs: {str(e)}"

    def deletar_job(self, job_id: int) -> bool:
        """Remove um job pelo ID."""
        try:
            self.worskpace.jobs.delete(job_id=job_id)
            return f"Job {job_id} deletado com sucesso."

        except Exception as e:
            return f"Erro ao deletar job: {str(e)}"

    def executar_job(self, job_id: int) -> bool:
        """Executa um job pelo ID."""
        try:
            run = self.worskpace.jobs.run_now(job_id=job_id)
            return f"Job {job_id} iniciado com sucesso. Run ID: {run.run_id}"

        except Exception as e:
            return f"Erro ao executar job: {str(e)}"

    def atualizar_job(self, job_id: int, novo_nome: str) -> str:
        """Atualiza o nome de um job."""
        try:
            self.worskpace.jobs.update(
                job_id=job_id, new_settings=JobSettings(name=novo_nome)
            )

            return f"Job {job_id} atualizado para '{novo_nome}'"

        except Exception as e:
            return f"Erro ao atualizar job: {str(e)}"

    def calcular_custo(self, run_id: int) -> str:
        """Consulta o custo via System Tables."""
        query = f"""
            SELECT SUM(usage_quantity * list_prices.pricing.default) as custo_estimado
            FROM system.billing.usage
            WHERE usage_metadata.job_run_id = '{run_id}'
            """

        response = self.worskpace.statement_execution.execute_statement(
            statement=query,
            warehouse_id=self.warehouse_id,  # ⚠️ obrigatório
        )

        # 🔥 pegar resultado
        if response.result and response.result.data_array:
            custo = float(response.result.data_array[0][0])
            return f"Custo estimado para o Run {run_id}: ${custo:.4f}"

        return "Custo não disponível ou Run ID inválido."

    def criar_dashboard_padrao(self) -> str:
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            caminho = os.path.join(
                base_dir, "..", "dashboard", "agent_monitoring_dashboard.lvdash.json"
            )

            if not os.path.exists(caminho):
                return "Erro: Arquivo do dashboard não encontrado."

            with open(caminho, "r") as f:
                conteudo_dashboard = json.load(f)

            # Construção do payload conforme exigido pela documentação da API Lakeview
            # O campo 'serialized_dashboard' precisa ser uma string JSON,
            # por isso usamos json.dumps() no objeto carregado.
            payload = {
                "display_name": "Agent Monitoring Dashboard",
                "warehouse_id": os.getenv("DATABRICKS_WAREHOUSE_ID"),
                "serialized_dashboard": json.dumps(conteudo_dashboard),
            }

            url = f"{os.getenv('DATABRICKS_HOST')}/api/2.0/lakeview/dashboards"

            headers = {
                "Authorization": f"Bearer {os.getenv('DATABRICKS_TOKEN')}",
                "Content-Type": "application/json",
            }

            response = requests.post(url, headers=headers, json=payload)

            if response.status_code != 200:
                return f"Erro na API ({response.status_code}): {response.text}"

            data = response.json()
            return f"Dashboard criado! ID: {data.get('dashboard_id')}"

        except Exception as e:
            return f"Erro inesperado: {str(e)}"

    def listar_modelos(self) -> str:
        # Busca a pasta 'models' na raiz do projeto
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Caminho relativo de src/infrastructure/adapters para a raiz é ../../../
        models_dir = os.path.join(base_dir, "..", "..", "..", "..", "models")

        # Normaliza o caminho para ser absoluto
        models_dir = os.path.abspath(models_dir)

        # Verifica se o diretório existe para evitar erros
        if not os.path.exists(models_dir):
            return "⚠️ Pasta 'models' não encontrada."

        arquivos = [f for f in os.listdir(models_dir) if f.endswith(".py")]

        if not arquivos:
            return "📂 Nenhum modelo (.py) encontrado na pasta."

        # Converte a lista para uma única string separada por vírgulas ou linhas
        # Usando emojis para ficar no padrão do seu Agente
        lista_formatada = "\n".join([f"📄 {arq}" for arq in arquivos])

        return f"🚀 **Modelos disponíveis para deploy:**\n{lista_formatada}"

    def upload_modelo(self, nome_arquivo: str) -> str:
        try:
            w = self.worskpace
            base_dir = os.path.dirname(os.path.abspath(__file__))
            local_path = os.path.abspath(
                os.path.join(base_dir, "..", "..", "..", "..", "models")
            )

            workspace_folder = "/Users/fabio.jdluz@gmail.com/models"
            workspace_path = f"{workspace_folder}/{nome_arquivo}"

            # 1. Cria a pasta
            w.workspace.mkdirs(path=workspace_folder)

            # 2. Upload com formato FORÇADO para SOURCE (Script Python)
            with open(local_path, "rb") as f:
                w.workspace.upload(
                    path=workspace_path,
                    content=f,
                    overwrite=True,
                    format=ImportFormat.AUTO,  # Isso diz ao Databricks: "trate como código fonte"
                )

            return workspace_path

        except Exception as e:
            return f"Erro ao subir modelo: {str(e)}"

        except Exception as e:
            return f"Erro ao subir modelo: {str(e)}"

    def criar_job_modelo(self, nome_arquivo: str, workspace_path: str) -> str:
        w = self.worskpace
        # O Spark entende caminhos absolutos do Workspace corretamente aqui
        job = w.jobs.create(
            name=f"Job - {nome_arquivo}",
            tasks=[
                Task(
                    task_key="model",
                    existing_cluster_id=self.cluster_id,
                    spark_python_task=SparkPythonTask(python_file=workspace_path),
                )
            ],
        )
        return job.job_id

    def deploy_modelo(self, nome_arquivo: str) -> str:
        try:
            workspace_path = self.upload_modelo(nome_arquivo)

            if isinstance(workspace_path, str) and "Erro" in workspace_path:
                return workspace_path

            job_id = self.criar_job_modelo(nome_arquivo, workspace_path)

            return (
                f"✅ Modelo enviado para: {workspace_path}\n🚀 Job criado! ID: {job_id}"
            )

        except Exception as e:
            return f"Erro no deploy: {str(e)}"

    def bundle_job_yaml(self) -> str:
        """
        Faz deploy do job YAML direto via REST API (sem conversão manual)
        """
        try:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            yaml_path = os.path.abspath(
                os.path.join(
                    base_dir, "..", "..", "..", "..", "models", "job_model.yaml"
                )
            )

            if not os.path.exists(yaml_path):
                return f"❌ YAML não encontrado: {yaml_path}"

            # =========================
            # LER YAML
            # =========================
            with open(yaml_path, "r") as f:
                config = yaml.safe_load(f)

            jobs = config["resources"]["jobs"]
            job_key = list(jobs.keys())[0]
            job_cfg = jobs[job_key]

            # =========================
            # CHAMAR API DIRETA
            # =========================
            url = f"{os.getenv('DATABRICKS_HOST')}/api/2.1/jobs/create"

            headers = {
                "Authorization": f"Bearer {os.getenv('DATABRICKS_TOKEN')}",
                "Content-Type": "application/json",
            }

            response = requests.post(
                url,
                headers=headers,
                json=job_cfg,  # 🔥 manda direto o YAML convertido
            )

            if response.status_code != 200:
                return {"status": "error", "message": response.text}

            data = response.json()

            if response.status_code != 200:
                return f"❌ Erro na API Databricks ({response.status_code}): {response.text}"

            data = response.json()
            job_id = data.get("job_id")
            job_name = job_cfg.get("name", "Unknown")

            # Retornando como string concatenada para o Agente
            return f"✅ Deploy realizado com sucesso! Job Name: '{job_name}' | ID: {job_id}"

        except Exception as e:
            return {"status": "error", "message": str(e)}

    def executar_pipeline_csv_para_feature_store(self) -> str:
        """
        Pipeline fixo:
        CSV local → Spark DataFrame → Delta Table → Feature Store (ou fallback Delta)
        """
        try:
            # Inicializa a sessão Spark
            spark = DatabricksSession.builder.getOrCreate()

            try:
                from databricks.feature_engineering import FeatureEngineeringClient

                fe = FeatureEngineeringClient()
            except ImportError:
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
                return f"⚠️ CSV não encontrado no caminho: {csv_path}"

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
                F.sum("preco").alias("valor_total"),
            )

            # =========================
            # FEATURE STORE (ou fallback)
            # =========================
            if fe:
                try:
                    fe.create_table(
                        name=feature_table_name,
                        primary_keys=["id_unico_cliente"],
                        df=df_features,
                    )
                except:
                    df_features.write.format("delta").mode("overwrite").saveAsTable(
                        feature_table_name
                    )
            else:
                df_features.write.format("delta").mode("overwrite").saveAsTable(
                    feature_table_name
                )

            # Retorno de sucesso (agora fora dos ifs para garantir que sempre retorne ao final do sucesso)
            return (
                f"✅ Pipeline executado com sucesso!\n"
                f"📍 Tabela Base (Delta): {base_table}\n"
                f"✨ Feature Store: {feature_table_name}\n"
                f"📊 Status: Ingestão e processamento concluídos."
            )

        except Exception as e:
            # Este except agora captura qualquer erro ocorrido no bloco principal
            return f"❌ Erro durante o processamento do pipeline de Feature Store: {str(e)}"

    def show_drift(self) -> str:
        """
        Calcula drift simples em uma tabela do Databricks Lake
        e retorna um relatório consolidado em string.
        """
        try:
            spark = DatabricksSession.builder.getOrCreate()

            # Leitura da tabela (usando sample para performance)
            df = spark.table("pedido.default.cliente").sample(0.05).toPandas()

            # --- DRIFT NUMÉRICO (KS) ---
            sample = df["preco"].sample(frac=0.5, random_state=42)
            rest = df["preco"].drop(sample.index)
            ks_stat, ks_p = ks_2samp(sample, rest)

            # --- DRIFT CATEGÓRICO (CHI2) ---
            s1 = df["status_pedido"].sample(frac=0.5, random_state=42)
            s2 = df["status_pedido"].drop(s1.index)
            c1, c2 = s1.value_counts(), s2.value_counts()
            cats = set(c1.index).union(set(c2.index))
            v1, v2 = [c1.get(x, 0) for x in cats], [c2.get(x, 0) for x in cats]
            chi2, chi_p, _, _ = chi2_contingency([v1, v2])

            # --- PSI SIMPLES ---
            expected = df["preco"].sample(frac=0.5, random_state=42)
            actual = df["preco"].drop(expected.index)
            e, a = (
                expected.value_counts(normalize=True),
                actual.value_counts(normalize=True),
            )
            all_keys = set(e.index).union(set(a.index))
            psi = sum(
                (a.get(k, 0.0001) - e.get(k, 0.0001))
                * np.log(a.get(k, 0.0001) / e.get(k, 0.0001))
                for k in all_keys
            )

            # --- FORMATAÇÃO DO RESULTADO ---
            has_drift = ks_p < 0.05 or chi_p < 0.05 or psi > 0.2
            status_icon = "⚠️ DRIFT DETECTADO" if has_drift else "✅ ESTÁVEL"

            return (
                f"📊 **Relatório de Monitoramento de Drift**\n\n"
                f"Status Geral: **{status_icon}**\n"
                f"---"
                f"\n🔹 **Teste KS (Preço):**\n"
                f"  - P-Value: {ks_p:.4f}\n"
                f"  - Drift: {'Sim' if ks_p < 0.05 else 'Não'}\n"
                f"\n🔹 **Teste Chi-Square (Status):**\n"
                f"  - P-Value: {chi_p:.4f}\n"
                f"  - Drift: {'Sim' if chi_p < 0.05 else 'Não'}\n"
                f"\n🔹 **Índice PSI:**\n"
                f"  - Valor: {psi:.4f}\n"
                f"  - Severidade: {'Alta' if psi > 0.2 else 'Baixa' if psi < 0.1 else 'Moderada'}"
            )

        except Exception as e:
            return f"❌ Erro ao calcular análise de drift: {str(e)}"
