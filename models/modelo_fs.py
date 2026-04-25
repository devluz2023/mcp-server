import os
from databricks.connect import DatabricksSession
from databricks.feature_engineering import FeatureEngineeringClient
from pyspark.sql import functions as F, SparkSession

def get_spark_and_fe_client():
    """Detecta o ambiente e inicializa as sessões."""
    if "DATABRICKS_RUNTIME_VERSION" in os.environ:
        spark = SparkSession.builder.getOrCreate()
    else:
        spark = DatabricksSession.builder.getOrCreate()
    
    fe = FeatureEngineeringClient()
    return spark, fe

def main():
    spark, fe = get_spark_and_fe_client()
    target_table = "pedido.default.cliente_features"
    pk_column = "id_unico_cliente"

    try:
        # 1. Processamento das Features
        df_raw = spark.table("pedido.default.cliente")
        df_features = df_raw.groupBy(pk_column).agg(
            F.count("id_pedido").alias("total_pedidos"),
            F.avg("preco").alias("ticket_medio"),
            F.sum("preco").alias("valor_total_gasto")
        )

        # 2. Tentativa de Registro ou Atualização
        try:
            print(f"Tentando registrar: {target_table}")
            fe.create_table(
                name=target_table,
                primary_keys=[pk_column],
                df=df_features,
                description="Agregados de Cliente - Feature Store"
            )
            print("Tabela registrada!")
        except Exception:
            print("A tabela já existe. Aplicando ajustes de estrutura e merge...")
            
            # Ajuste de schema: O Unity Catalog exige que a PK seja NOT NULL
            spark.sql(f"ALTER TABLE {target_table} ALTER COLUMN {pk_column} SET NOT NULL")
            
            # Adiciona a Constraint de PK se ainda não existir
            try:
                spark.sql(f"""
                    ALTER TABLE {target_table} 
                    ADD CONSTRAINT {target_table.split('.')[-1]}_pk 
                    PRIMARY KEY ({pk_column})
                """)
            except Exception:
                pass # Constraint já existe, podemos prosseguir
            
            # Atualização dos dados
            fe.write_table(
                name=target_table,
                df=df_features,
                mode="merge"
            )
            print("Dados atualizados com sucesso via Merge!")

        # 3. Governança
        spark.sql(f"COMMENT ON TABLE {target_table} IS 'Feature Store: Agregados de Cliente'")
        print("Processo finalizado!")

    except Exception as e:
        print(f"Erro crítico: {str(e)}")
        raise e

if __name__ == "__main__":
    main()