import debugpy
import time

print("--- Iniciando teste ---")
# Força o bind no IP correto
debugpy.listen(("0.0.0.0", 5678))
print("--- Aguardando VS Code ---")
debugpy.wait_for_client()
print("--- Conectado! ---")

while True:
    print("Processo vivo...")
    time.sleep(10)