from langchain_chroma import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

# 1. Carrega o modelo de embedding (o mesmo que você usava)
embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# 2. Inicializa o Chroma (ele cria a pasta 'chroma_db' automaticamente para persistir os dados)
db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_function)

# 3. Adiciona sua base de conhecimento (só precisa rodar uma vez!)
kb = ["Erro de conexão Databricks: Verifique o cluster.", "OOM: Aumente o memory da task."]
# O Chroma gerencia os vetores internamente, não precisamos mais do np.dot
db.add_texts(kb)

def analisar_log(log_texto: str):
    # O Chroma busca o documento mais parecido semanticamente
    results = db.similarity_search(log_texto, k=1)
    return results[0].page_content



def salvar_contexto(texto, resposta):
    db.add_texts([f"Log: {texto} | Resposta: {resposta}"])


def buscar_contexto(log_texto):
    resultados = db.similarity_search_with_score(log_texto, k=1)
    if resultados and resultados[0][1] < 0.2:
        return resultados[0].page_content.split(" | Resposta: ")[-1]
    return None