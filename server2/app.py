import debugpy
import time
import os
from agent import  orquestrador_po

if os.getenv("DEBUG") == "1":
    debugpy.listen(("0.0.0.0", 5678))
    # Removemos o wait_for_client() para não travar o início
    print("--- Debugger pronto para conexão ---")

while True:
    print("Processo vivo...")
    
    # Isso diz ao debugger: "Se o VS Code estiver conectado, PAUSE AQUI"
    # Se não estiver conectado, ele ignora e continua rodando.
    debugpy.breakpoint() 
    
    orquestrador_po("Tenho 100 de água e 50 de terra. Tomate gasta 2 de água e 1 de terra. Alface gasta 1 de água e 2 de terra. Tomate lucra 5 e Alface lucra 4. Maximize o lucro.")
    time.sleep(10)