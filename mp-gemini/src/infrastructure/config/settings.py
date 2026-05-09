import os

from dotenv import find_dotenv, load_dotenv

# Carrega o .env da raiz automaticamente
load_dotenv(find_dotenv())


class Settings:
    @property
    def openai_api_key(self) -> str:
        return self._get_env("OPENAI_API_KEY")

    @property
    def databricks_host(self) -> str:
        return self._get_env("DATABRICKS_HOST")

    @property
    def databricks_token(self) -> str:
        return self._get_env("DATABRICKS_TOKEN")

    def _get_env(self, key: str) -> str:
        value = os.getenv(key)
        if not value:
            raise ValueError(f"Variável {key} não encontrada no .env!")
        return value


settings = Settings()
