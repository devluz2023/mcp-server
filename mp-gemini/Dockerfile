# Imagem base leve
FROM python:3.11-slim

# Evita gerar arquivos .pyc
ENV PYTHONDONTWRITEBYTECODE=1

# Evita buffer no stdout
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /app

# Copia requirements primeiro (melhor cache)
COPY requirements.txt .

# Instala dependências
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copia o resto do projeto
COPY . .

# Porta do Streamlit
EXPOSE 8501

# Comando para rodar app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]