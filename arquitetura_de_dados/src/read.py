from databricks.connect import DatabricksSession

# 1. Inicializa a sessão
spark = DatabricksSession.builder.getOrCreate()

# 2. Define o nome da tabela que você acabou de criar
full_table_name = "pedido.default.cliente"

print(f"Lendo dados da tabela: {full_table_name}...")

# 3. Lê os dados da Delta Table
# O .table() é a forma mais performática e recomendada no Unity Catalog
df = spark.table(full_table_name)

# 4. Exibe os resultados
print("Primeiras 10 linhas:")
df.show(10)

# 5. Opcional: Exibe o esquema para validar os tipos de dados
print("Esquema da Tabela:")
df.printSchema()

# 6. Exemplo de contagem (para validar a carga)
print(f"Total de registros: {df.count()}")



