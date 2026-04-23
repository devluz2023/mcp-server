import mlflow
import pandas as pd
from scipy.stats import ks_2samp
from pyspark.sql import SparkSession
import logging

def executar_pipeline_drift():
    spark = SparkSession.builder.getOrCreate()
    table_path = "samples.accuweather.forecast_daily_calendar_imperial"
    # Adicionando has_ice para teste
    colunas_interesse = ["minutes_of_rain_total", "minutes_of_snow_total", "has_ice"]
    
    # 1. Leitura e Conversão
    df_spark = spark.read.table(table_path).select(*colunas_interesse).limit(2000)
    df = df_spark.toPandas()

    # 2. Split
    ref = df.iloc[:1000]
    cur = df.iloc[1000:]

    mlflow.set_experiment("/Users/fabio.jdluz@gmail.com/drift_analysis_red_flag")
    
    with mlflow.start_run(run_name="Drift_Fix_Nulos"):
        for col in colunas_interesse:
            # LIMPEZA: Remove NAs para o teste não quebrar
            ref_clean = ref[col].dropna()
            cur_clean = cur[col].dropna()

            # Valida se temos dados suficientes após a limpeza
            if len(ref_clean) > 0 and len(cur_clean) > 0:
                try:
                    stat, p_value = ks_2samp(ref_clean, cur_clean)
                    drift_detected = p_value < 0.05
                    
                    mlflow.log_metric(f"p_value_{col}", p_value)
                    print(f"Coluna: {col.ljust(25)} | P-Value: {p_value:.4f}")
                except Exception as e:
                    print(f"Erro ao calcular drift para {col}: {e}")
            else:
                print(f"Coluna: {col.ljust(25)} | Status: Sem dados suficientes (Nulos)")

        print("✅ Processo concluído (com tratamento de nulos).")

if __name__ == "__main__":
    executar_pipeline_drift()