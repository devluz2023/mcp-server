from sentence_transformers import SentenceTransformer, util
import torch
from rag_engine import buscar_contexto, salvar_contexto # Apenas lógica, sem libs de DB
# Carregue o modelo apenas uma vez, fora da função, para não recarregar toda hora
bert_model = SentenceTransformer('bert-base-multilingual-cased')

def classificar_urgencia(log_texto):
    # Frases de referência para erros graves
    criticos = [
        "CRITICAL error", 
        "FATAL failure in system", 
        "INTERNAL_ERROR_ATTRIBUTE_NOT_FOUND", 
        "Database connection timeout"
    ]
    
    # Gera os embeddings (vetores)
    log_embedding = bert_model.encode(log_texto, convert_to_tensor=True)
    criticos_embeddings = bert_model.encode(criticos, convert_to_tensor=True)
    
    # Calcula a similaridade de cosseno
    # Retorna uma lista de scores (0 a 1)
    scores = util.cos_sim(log_embedding, criticos_embeddings)
    
    # Pega o maior score (o erro que mais se parece com um erro crítico)
    max_score = torch.max(scores).item()
    
    # Define um limite (threshold)
    return "ALTA" if max_score > 0.6 else "NORMAL"



def classificar_resultado_teste(output_teste):
    """
    Classifica se o teste passou ou falhou baseado no output.
    """
    referencias = ["test passed", "successfully completed", "assertion error", "test failed"]
    
    output_embedding = bert_model.encode(output_teste, convert_to_tensor=True)
    ref_embeddings = bert_model.encode(referencias, convert_to_tensor=True)
    
    scores = util.cos_sim(output_embedding, ref_embeddings)
    
    # 0: test passed, 1: successfully, 2: assertion error, 3: test failed
    max_score_idx = torch.argmax(scores).item()
    
    if max_score_idx in [0, 1]:
        return "PASSOU"
    else:
        return "FALHOU"
    


def processar_ou_recuperar(log_texto, funcao_processamento):
    # Tenta recuperar do RAG
    contexto = buscar_contexto(log_texto)
    if contexto:
        return contexto
    
    # Se não existe, processa
    resultado = funcao_processamento(log_texto)
    
    # Salva no RAG
    salvar_contexto(log_texto, resultado)
    
    return resultado