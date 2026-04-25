import os
from databricks.connect import DatabricksSession
from databricks.feature_engineering import FeatureEngineeringClient
from pyspark.sql import functions as F, SparkSession

def get_spark_and_fe_client():
    """Detecta o ambiente e retorna as sessões configuradas."""
    try:
        # Tenta detectar se estamos no cluster (Runtime) ou local (Connect)
        if "DATABRICKS_RUNTIME_VERSION" in os.environ:
            spark = SparkSession.builder.getOrCreate()
        else:
            spark = DatabricksSession.builder.getOrCreate()
        
        fe = FeatureEngineeringClient()
        return spark, fe
    except Exception as e:
        print(f"Erro ao inicializar sessão: {e}")
        raise

# 1. Inicializa o ambiente
spark, fe = get_spark_and_fe_client()

# 2. Configurações da Tabela
target_table = "pedido.default.cliente_features"

# 3. Processamento das Features
# Aqui você pode mudar a estrutura (adicionar novas colunas/agregados) livremente
df_raw = spark.table("pedido.default.cliente")

df_features = df_raw.groupBy("id_unico_cliente").agg(
    F.count("id_pedido").alias("total_pedidos"),
    F.avg("preco").alias("ticket_medio"),
    F.sum("preco").alias("valor_total_gasto") # Exemplo: nova coluna adicionada
)

# 4. Criação ou Atualização com Evolução de Esquema
# Se a tabela não existe, cria. Se existe e a estrutura mudou, sobrescreve o esquema.
try:
    print(f"Tentando registrar a feature table: {target_table}")
    fe.create_table(
        name=target_table,
        primary_keys=["id_unico_cliente"],
        df=df_features
    )
    print("Tabela registrada com sucesso!")
except Exception:
    print("A tabela já existe. Atualizando estrutura e dados...")
    # O uso do overwriteSchema permite que você mude as colunas do df_features 
    # e a tabela no Unity Catalog seja atualizada automaticamente.
    df_features.write \
        .format("delta") \
        .mode("overwrite") \
        .option("overwriteSchema", "true") \
        .saveAsTable(target_table)
    print("Esquema e dados atualizados com sucesso!")

# 5. Comentário de governança
spark.sql(f"COMMENT ON TABLE {target_table} IS 'Feature Store: Agregados de Cliente - Atualizado em 2026'")

print("Processo finalizado com sucesso!")