from databricks.connect import DatabricksSession
import pandas as pd
import os

# 1. Inicializa a sessão
spark = DatabricksSession.builder.getOrCreate()

# 2. Definições (Como o catálogo 'pedido' já existe)
CATALOGO = "pedido"
SCHEMA = "default" # Ou o nome do seu schema preferido
TABELA = "cliente"
FULL_TABLE_NAME = f"{CATALOGO}.{SCHEMA}.{TABELA}"

# 3. Cria o Schema (caso ainda não exista)
print(f"Verificando/Criando schema {SCHEMA} no catálogo {CATALOGO}...")
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {CATALOGO}.{SCHEMA}")

# 4. Leitura do arquivo CSV local
local_csv_path = "/Users/fabiojuliodaluz/Documents/GitHub/mcp-server/arquitetura_de_dados/data/BancoDeDados.csv"

if os.path.exists(local_csv_path):
    print("Lendo CSV e convertendo para Spark...")
    df_pandas = pd.read_csv(local_csv_path)
    df_spark = spark.createDataFrame(df_pandas)
    
    # 5. Gravação da tabela
    # Como o catálogo já existe, o Databricks usará o Managed Location 
    # que foi definido quando o catálogo 'pedido' foi criado.
    print(f"Gravando na tabela: {FULL_TABLE_NAME}...")
    df_spark.write \
        .format("delta") \
        .mode("overwrite") \
        .saveAsTable(FULL_TABLE_NAME)
        
    print("Carga finalizada com sucesso!")
else:
    print(f"Erro: O arquivo {local_csv_path} não foi encontrado.")