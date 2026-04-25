from databricks.connect import DatabricksSession
from pyspark.sql import functions as F

# 1. Inicializa a sessão (Modo de leitura apenas)
spark = DatabricksSession.builder.getOrCreate()

# 2. Definições das tabelas
tabela_fonte = "pedido.default.cliente"
tabela_features = "pedido.default.cliente_features"

print(f"--- Comparação de Tabelas ---")

# 3. Leitura dos DataFrames
df_fonte = spark.table(tabela_fonte)
df_features = spark.table(tabela_features)

# 4. Comparação de contagem de registros
total_fonte = df_fonte.count()
total_features = df_features.count()

print(f"Total registros na Tabela Fonte: {total_fonte}")
print(f"Total registros na Feature Store: {total_features}")

# 5. Verificação de ID (Garante que os clientes são os mesmos)
# Verifica se há IDs na feature que não estão na fonte
diff_count = df_features.select("id_unico_cliente") \
    .subtract(df_fonte.select("id_unico_cliente")) \
    .count()

if diff_count == 0:
    print("Status: Todos os IDs da Feature Store existem na Tabela Fonte (Integridade OK).")
else:
    print(f"Status: ALERTA! Existem {diff_count} IDs na Feature Store que não estão na Fonte.")

# 6. Comparação de Schema (Visualiza se as estruturas são compatíveis)
print("\n--- Comparação de Esquema ---")
print("Colunas da Tabela Fonte:")
print(df_fonte.columns)
print("\nColunas da Feature Store:")
print(df_features.columns)

print("\n--- Processo de comparação finalizado ---")

# 7. Comparação de Quantidade de Colunas e Linhas
num_cols_fonte = len(df_fonte.columns)
num_cols_features = len(df_features.columns)

print("\n--- Verificação de Estrutura ---")
print(f"Número de colunas na Fonte: {num_cols_fonte}")
print(f"Número de colunas na Feature Store: {num_cols_features}")

if num_cols_fonte == num_cols_features:
    print("Status: O número de colunas é IDÊNTICO.")
else:
    print(f"Status: DIFERENÇA DE COLUNAS! A diferença é de {abs(num_cols_fonte - num_cols_features)} colunas.")

# Comparação de Linhas
if total_fonte == total_features:
    print(f"Status: O número de linhas é IDÊNTICO ({total_fonte} registros).")
else:
    print(f"Status: DIFERENÇA DE LINHAS! Fonte: {total_fonte} | Features: {total_features}")