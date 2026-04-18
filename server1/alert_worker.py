import docker
import time
import requests

client = docker.from_env()

def enviar_alerta(container_nome, erro):
    mensagem = f"🚨 ALERTA: O container {container_nome} caiu! Motivo: {erro}"
    print(mensagem)
    # Exemplo: Enviar para um webhook (Slack, Discord, Teams)
    # requests.post("SUA_URL_WEBHOOK", json={"text": mensagem})

def monitorar_containers():
    containers_alvo = ["logistica-sku-analytics"]
    while True:
        for nome in containers_alvo:
            try:
                container = client.containers.get(nome)
                if container.status != "running":
                    enviar_alerta(nome, container.status)
            except docker.errors.NotFound:
                enviar_alerta(nome, "Container não encontrado (Crash ou Remoção)")
        
        time.sleep(10) # Verifica a cada 10 segundos

if __name__ == "__main__":
    monitorar_containers()