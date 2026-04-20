import logging
from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

# Configuração do logger
logger = logging.getLogger("RAGEngine")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 1. Carrega o modelo de embedding
logger.info("Carregando modelo de embeddings...")
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# 2. Inicializa o Chroma
logger.info("Conectando ao banco vetorial ChromaDB...")
db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)

# 3. Adiciona sua base de conhecimento
def inicializar_db():
    logger.info("Verificando/Adicionando base de conhecimento inicial...")
    kb = ["Erro de conexão Databricks: Verifique o cluster.", "OOM: Aumente o memory da task."]
    db.add_texts(kb)
    logger.info("Base de conhecimento carregada.")

def analisar_log(log_texto: str):
    logger.info("Executando busca por similaridade para o log...")
    results = db.similarity_search(log_texto, k=1)
    
    if results:
        logger.info(f"Log analisado. Contexto encontrado: {results[0].page_content[:50]}...")
        return results[0].page_content
    
    logger.warning("Nenhum contexto encontrado para o log.")
    return None

def salvar_contexto(texto, resposta):
    logger.info("Persistindo novo contexto no banco de vetores...")
    try:
        db.add_texts([f"Log: {texto} | Resposta: {resposta}"])
        logger.info("Contexto salvo com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao salvar contexto no Chroma: {str(e)}")

def buscar_contexto(log_texto):
    logger.info("Consultando RAG por contexto prévio...")
    resultados = db.similarity_search_with_score(log_texto, k=1)
    
    if resultados:
        doc, score = resultados[0]
        # O Chroma usa distância Euclidiana ao quadrado ou cosseno, 
        # verifique a métrica configurada no seu Chroma. 
        # Abaixo assumimos que score baixo é melhor (distância).
        logger.info(f"Resultado encontrado com score: {score:.4f}")
        
        if score < 0.2:
            resposta = doc.page_content.split(" | Resposta: ")[-1]
            logger.info("Contexto relevante validado pelo threshold.")
            return resposta
        else:
            logger.info("Score acima do threshold. Ignorando contexto.")
            
    return None