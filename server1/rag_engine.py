import logging
import os
from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

# Configuração de Logs
logger = logging.getLogger("RAGEngine")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# --- CARREGAMENTO ÚNICO (Singleton Pattern) ---
# Isso evita o recarregamento do modelo a cada requisição
class RAGManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RAGManager, cls).__new__(cls)
            logger.info("Inicializando RAG Manager e modelo de Embeddings...")
            # Caminho otimizado para cache
            cls._instance.embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
            cls._instance.db = Chroma(
                persist_directory="./chroma_db", 
                embedding_function=cls._instance.embeddings
            )
            # Inicializa a KB se necessário
            cls._instance._init_kb()
        return cls._instance

    def _init_kb(self):
        # Verifica se já existem documentos para evitar duplicidade
        # (Opcional: você pode checar se a KB está vazia antes de adicionar)
        kb = ["Erro de conexão Databricks: Verifique o cluster.", "OOM: Aumente o memory da task."]
        self.db.add_texts(kb)
        logger.info("Base de conhecimento inicial carregada.")

# Instância única para uso global
rag = RAGManager()

# --- FUNÇÕES DE INTERFACE ---

def analisar_log(log_texto: str):
    """Analisa logs e retorna uma resposta baseada na similaridade."""
    logger.info("Executando busca por similaridade...")
    results = rag.db.similarity_search(log_texto, k=1)
    
    if results:
        return results[0].page_content
    return "Status: NORMAL (Nenhum padrão crítico detectado)"

def salvar_contexto(texto, resposta):
    """Persiste novos logs e diagnósticos no ChromaDB."""
    try:
        rag.db.add_texts([f"Log: {texto} | Resposta: {resposta}"])
        logger.info("Contexto salvo no ChromaDB.")
    except Exception as e:
        logger.error(f"Erro ao salvar no banco: {str(e)}")

def buscar_contexto(log_texto):
    """Busca contexto prévio para evitar reprocessamento."""
    resultados = rag.db.similarity_search_with_score(log_texto, k=1)
    
    if resultados:
        doc, score = resultados[0]
        # Score menor que 0.2 indica alta similaridade
        if score < 0.2:
            logger.info(f"Cache RAG encontrado (Score: {score:.4f})")
            return doc.page_content.split(" | Resposta: ")[-1]
    
    return None