from abc import ABC, abstractmethod


class JobRepository(ABC):
    """
    Interface de Domínio para operações no Databricks.
    """

    @abstractmethod
    def criar_job(self, job: str) -> str:
        """Recebe a Entidade Job, persiste no Databricks e retorna com ID preenchido."""
        pass

    @abstractmethod
    def listar_jobs(self) -> str:
        """Recupera a lista de todos os Jobs como Entidades de Domínio."""
        pass

    @abstractmethod
    def deletar_job(self, job_id: int) -> bool:
        """Remove o job do workspace através do ID."""
        pass

    @abstractmethod
    def executar_job(self, job_id: int) -> bool:
        """Dispara a execução imediata de um job."""
        pass

    @abstractmethod
    def atualizar_job(self, job_id: int, novo_nome: str) -> str:
        """Atualiza o nome de um job."""
        pass

    @abstractmethod
    def calcular_custo(self, run_id: int) -> str:
        """Consulta o custo via System Tables."""
        pass

    @abstractmethod
    def criar_dashboard_padrao(self) -> str:
        pass

    @abstractmethod
    def listar_modelos(self) -> str:
        pass

    @abstractmethod
    def upload_modelo(self, nome_arquivo: str) -> str:
        pass

    @abstractmethod
    def criar_job_modelo(nome_arquivo: str, workspace_path: str) -> str:
        pass

    @abstractmethod
    def deploy_modelo(self, nome_arquivo: str) -> str:
        pass

    @abstractmethod
    def bundle_job_yaml(self) -> str:
        """
        Faz deploy do job YAML direto via REST API (sem conversão manual)
        """
        pass

    @abstractmethod
    def executar_pipeline_csv_para_feature_store(self) -> str:
        """
        Pipeline fixo:
        CSV local → Spark DataFrame → Delta Table → Feature Store (ou fallback Delta)
        """
        pass

    @abstractmethod
    def show_drift(self) -> str:
        pass
