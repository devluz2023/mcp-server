from dataclasses import dataclass

@dataclass
class DatabricksJob:
    job_id: int
    name: str
    status: str = "unknown"