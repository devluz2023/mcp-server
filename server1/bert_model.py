import logging
from sentence_transformers import SentenceTransformer, util
import torch
from rag_engine import buscar_contexto, salvar_contexto

# Configuração do logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

bert_model = SentenceTransformer('bert-base-multilingual-cased')

def classificar_urgencia(log_texto):
    criticos = [
        "CRITICAL error", 
        "FATAL failure in system", 
        "INTERNAL_ERROR_ATTRIBUTE_NOT_FOUND", 
        "Database connection timeout"
    ]
    
    logger.info("Calculando urgência para o log fornecido.")
    
    log_embedding = bert_model.encode(log_texto, convert_to_tensor=True)
    criticos_embeddings = bert_model.encode(criticos, convert_to_tensor=True)
    
    scores = util.cos_sim(log_embedding, criticos_embeddings)
    max_score = torch.max(scores).item()
    
    urgencia = "ALTA" if max_score > 0.6 else "NORMAL"
    
    # Logando o score para fins de ajuste (tuning) do threshold
    logger.info(f"Urgência classificada como {urgencia} (Max Score: {max_score:.4f})")
    
    return urgencia

def classificar_resultado_teste(output_teste):
    referencias = ["test passed", "successfully completed", "assertion error", "test failed"]
    
    logger.info("Analisando output de teste...")
    
    output_embedding = bert_model.encode(output_teste, convert_to_tensor=True)
    ref_embeddings = bert_model.encode(referencias, convert_to_tensor=True)
    
    scores = util.cos_sim(output_embedding, ref_embeddings)
    max_score_idx = torch.argmax(scores).item()
    
    resultado = "PASSOU" if max_score_idx in [0, 1] else "FALHOU"
    
    logger.info(f"Resultado do teste: {resultado} (Referência detectada: '{referencias[max_score_idx]}')")
    
    return resultado

def processar_ou_recuperar(log_texto, funcao_processamento):
    logger.info("Consultando RAG por contexto existente...")
    
    contexto = buscar_contexto(log_texto)
    if contexto:
        logger.info("Contexto encontrado no RAG. Retornando valor em cache.")
        return contexto
    
    logger.info("Contexto não encontrado. Executando processamento...")
    try:
        resultado = funcao_processamento(log_texto)
        salvar_contexto(log_texto, resultado)
        logger.info("Processamento concluído e salvo no RAG.")
        return resultado
    except Exception as e:
        logger.error(f"Erro ao processar/salvar contexto: {str(e)}")
        raise e