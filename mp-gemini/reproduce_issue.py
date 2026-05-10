import os
import sys

# Adiciona o diretório atual ao sys.path para importações funcionarem
sys.path.append(os.getcwd())

# Mock do settings para evitar carregar variáveis de ambiente reais que podem faltar

# Importa o JobAdapter
from src.infrastructure.adapters.job_adapter import JobAdapter


def test_listar_modelos():
    adapter = JobAdapter()
    resultado = adapter.listar_modelos()
    print(f"Resultado de listar_modelos: {resultado}")

    if "⚠️ Pasta 'models' não encontrada." in resultado:
        print("FALHA: Pasta 'models' ainda não foi encontrada.")
    elif "📂 Nenhum modelo (.py) encontrado na pasta." in resultado:
        print(
            "SUCESSO: Pasta 'models' encontrada, mas está vazia (comportamento esperado)."
        )
    elif "🚀 **Modelos disponíveis para deploy:**" in resultado:
        print("SUCESSO: Pasta 'models' encontrada e contém arquivos.")
    else:
        print(f"Resultado inesperado: {resultado}")


if __name__ == "__main__":
    # Garante que a pasta models existe na raiz
    if not os.path.exists("models"):
        os.makedirs("models")
        print("Pasta 'models' criada para o teste.")

    test_listar_modelos()
