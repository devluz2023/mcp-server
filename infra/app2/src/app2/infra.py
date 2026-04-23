from pyspark.sql import SparkSession

def setup_red_flag_infra():
    spark = SparkSession.builder.getOrCreate()
    
    print("--- Analisando Catálogos Disponíveis ---")
    catalogs_df = spark.sql("SHOW CATALOGS").collect()
    all_catalogs = [row['catalog'] for row in catalogs_df]
    
    # Filtro: Ignora os reservados e foca no seu catálogo de 'Work' (wk_...)
    target_catalog = next((c for c in all_catalogs if c.startswith('wk_')), None)
    
    if not target_catalog:
        print("❌ Nenhum catálogo de escrita (wk_*) encontrado!")
        return
        
    print(f"--- Usando Catálogo de Trabalho: {target_catalog} ---")
    
    try:
        # 1. Criar o Schema para o projeto Red Flag
        # Note: Não tentamos criar o catálogo, pois ele já existe e você tem permissão nele.
        spark.sql(f"CREATE SCHEMA IF NOT EXISTS {target_catalog}.sku_analytics_logs")
        
        # 2. Criar o Volume para os relatórios de Drift
        spark.sql(f"CREATE VOLUME IF NOT EXISTS {target_catalog}.sku_analytics_logs.drift_reports")
        
        volume_path = f"/Volumes/{target_catalog}/sku_analytics_logs/drift_reports"
        print(f"✅ Infraestrutura pronta em: {volume_path}")
        
    except Exception as e:
        print(f"❌ Erro ao configurar schema/volume: {e}")

if __name__ == "__main__":
    setup_red_flag_infra()