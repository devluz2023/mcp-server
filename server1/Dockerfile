# Use uma imagem leve de Python
FROM python:3.11-slim

# Instale dependências de sistema necessárias para o Docker e RAG
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instale as dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código
COPY . .

# Expõe a porta do Streamlit
EXPOSE 8501

# Comando para iniciar a aplicação
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]