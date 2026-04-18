import time

def main():
    print("Iniciando serviço de SKU Analytics...")
    # Aqui entraria a lógica principal do seu pipeline
    while True:
        print("Serviço rodando... monitorando SKU")
        # Simula o trabalho
        time.sleep(60) # Pausa por 60 segundos antes de rodar de novo

if __name__ == "__main__":
    main()