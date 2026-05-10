from dataclasses import dataclass
from typing import Optional


@dataclass
class Job:
    """
    Entidade de Domínio que representa um Job no Databricks.
    """

    job_id: int
    name: str
    cluster_id: Optional[str] = None
    notebook_path: Optional[str] = None
    status: str = "unknown"
    task_key: str = "main_task"  # Valor padrão para evitar erros no SDK
