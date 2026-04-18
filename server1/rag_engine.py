from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')

# Simulação de base de conhecimento sobre problemas de SKU Analytics
kb = ["Erro de conexão Databricks: Verifique o cluster.", "OOM: Aumente o memory da task."]
embeddings_kb = model.encode(kb)

def analisar_log(log_texto: str):
    log_emb = model.encode([log_texto])
    # Similaridade simples
    scores = np.dot(embeddings_kb, log_emb.T)
    return kb[np.argmax(scores)]