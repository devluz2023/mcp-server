import pandas as pd
from scipy.stats import ks_2samp
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, BooleanType
import datetime

def calcular_e_gravar_drift():
    spark = SparkSession.builder.getOrCreate()
    
    # --- 1. IDENTIFICAÇÃO DINÂMICA DO CATÁLOGO (Reutilizando sua lógica) ---
    catalogs_df = spark.sql("SHOW CATALOGS").collect()
    all_catalogs = [row['catalog'] for row in catalogs_df]
    target_catalog = next((c for c in all_catalogs if c.startswith('wk_')), None)
    
    if not target_catalog:
        print("❌ Catálogo wk_* não encontrado!")
        return

    schema_name = f"{target_catalog}.sku_analytics_logs"
    table_name = f"{schema_name}.drift_results"
    
    # --- 2. LEITURA DOS DADOS (Referência e Atual) ---
    source_table = "samples.accuweather.forecast_daily_calendar_imperial"
    colunas_interesse = ["minutes_of_rain_total", "minutes_of_snow_total"]
    
    # Pegamos uma amostra para o teste
    df_full = spark.read.table(source_table).select(*colunas_interesse).limit(2000).toPandas()
    ref = df_full.iloc[:1000]
    cur = df_full.iloc[1000:]

    results = []
    timestamp_exec = datetime.datetime.now()

    # --- 3. CÁLCULO DO DRIFT (KS Test) ---
    for col in colunas_interesse:
        ref_clean = ref[col].dropna()
        cur_clean = cur[col].dropna()

        if len(ref_clean) > 0 and len(cur_clean) > 0:
            stat, p_value = ks_2samp(ref_clean, cur_clean)
            drift_detected = p_value < 0.05
            
            results.append((
                timestamp_exec.strftime("%Y-%m-%d %H:%M:%S"),
                col, 
                float(p_value), 
                bool(drift_detected)
            ))

    # --- 4. GRAVAÇÃO NA DELTA TABLE ---
    # Criamos o DataFrame de resultados
    schema = StructType([
        StructField("execution_date", StringType(), True),
        StructField("column_name", StringType(), True),
        StructField("p_value", DoubleType(), True),
        StructField("drift_detected", BooleanType(), True)
    ])
    
    results_df = spark.createDataFrame(results, schema)

    print(f"--- Gravando resultados em: {table_name} ---")
    # Append para manter histórico de drifts passados
    results_df.write.format("delta").mode("append").saveAsTable(table_name)

    # --- 5. LEITURA E EXIBIÇÃO ---
    print("\n--- Histórico de Drift Atualizado ---")
    historico_df = spark.read.table(table_name).orderBy(F.desc("execution_date"))
    historico_df.show()

if __name__ == "__main__":
    calcular_e_gravar_drift()