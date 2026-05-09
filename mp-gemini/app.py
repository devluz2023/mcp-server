# main.py na raiz
import os
import subprocess
import sys


def run_app():
    # Caminho para o seu arquivo de interface dentro da pasta
    # Use o caminho a partir da pasta onde o main.py está localizado
    # main.py (raiz)
    app_path = os.path.join("src", "interfaces", "streamlit_app", "main.py")

    print("Iniciando o Assistente Databricks...")

    # Chama o streamlit como um subprocesso
    process = subprocess.Popen([sys.executable, "-m", "streamlit", "run", app_path])

    try:
        process.wait()
    except KeyboardInterrupt:
        print("\nFinalizando aplicação...")
        process.terminate()


if __name__ == "__main__":
    run_app()
