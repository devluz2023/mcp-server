import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Carrega o arquivo .env se ele existir
load_dotenv()


@dataclass(frozen=True)
class Config:
    """Configurações centralizadas da aplicação."""

    # LLM
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Databricks
    DATABRICKS_HOST: str = os.getenv("DATABRICKS_HOST", "")
    DATABRICKS_TOKEN: str = os.getenv("DATABRICKS_TOKEN", "")
    DATABRICKS_WAREHOUSE_ID: str = os.getenv("DATABRICKS_WAREHOUSE_ID", "")
    DATABRICKS_CLUSTER_ID: str = os.getenv("DATABRICKS_CLUSTER_ID", "")

    # Git / DevOps
    PERSONAL_ACCESS_TOKEN: str = os.getenv("PERSONAL_ACCESS_TOKEN", "")
    ORGANIZATION_URL: str = os.getenv("ORGANIZATION_URL", "")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "")
    REPOSITORY_NAME: str = os.getenv("REPOSITORY_NAME", "")
    BRANCH_NAME: str = os.getenv("BRANCH_NAME", "main")

    def validate(self):
        """Validação básica para garantir que as chaves críticas existem."""
        missing = [k for k, v in self.__dict__.items() if not v and "BRANCH" not in k]
        if missing:
            print(f"⚠️  Aviso: Variáveis de ambiente faltando: {', '.join(missing)}")


# Instância única para ser usada em toda a aplicação
settings = Config()
