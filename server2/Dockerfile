FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y -qq glpk-utils 

# Copia os requisitos e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia TODO o conteúdo da pasta (incluindo a pasta src e o main.py dentro dela)
COPY . .

# Comando para rodar o arquivo exatamente onde ele está na estrutura
CMD ["python", "app.py"]
