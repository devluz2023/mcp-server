import numpy as np
import pandas as pd
from pyspark.sql import SparkSession
from sklearn.cluster import KMeans
from xgboost import XGBRegressor
from catboost import CatBoostRegressor
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import StandardScaler

def train_complex_ensemble():
    spark = SparkSession.builder.getOrCreate()
    
    # 1. SIMULAÇÃO DE DADOS (Substitua pela sua tabela Delta)
    # Imaginando séries temporais de sensores ou logs
    data = np.random.rand(1000, 10, 5)  # 1000 amostras, 10 timesteps, 5 features
    target = np.random.rand(1000, 1)
    
    # --- PASSO 1: LSTM PARA EXTRAÇÃO DE FEATURES ---
    print("--- Treinando LSTM Extrator ---")
    lstm_model = Sequential([
        LSTM(64, input_shape=(10, 5), return_sequences=False),
        Dense(32, activation='relu') # Esta camada servirá como nosso vetor de características
    ])
    lstm_model.compile(optimizer='adam', loss='mse')
    lstm_model.fit(data, target, epochs=5, batch_size=32, verbose=0)
    
    # Extraímos as features da última camada densa
    features_lstm = lstm_model.predict(data)
    
    # --- PASSO 2: CLUSTERING (Segmentação de Comportamento) ---
    print("--- Gerando Clusters ---")
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(features_lstm)
    
    # Unimos as features da LSTM com o rótulo do Cluster
    X_ensemble = np.column_stack((features_lstm, clusters))
    
    # --- PASSO 3: ENSEMBLE (XGBOOST + CATBOOST) ---
    print("--- Treinando Ensemble (XGB + Cat) ---")
    
    # Modelo A: XGBoost
    xgb = XGBRegressor(n_estimators=100, learning_rate=0.05)
    xgb.fit(X_ensemble, target.ravel())
    
    # Modelo B: CatBoost
    cat = CatBoostRegressor(iterations=100, learning_rate=0.05, verbose=0)
    cat.fit(X_ensemble, target.ravel())
    
    # Predição Final (Média Simples - Voting)
    preds_xgb = xgb.predict(X_ensemble)
    preds_cat = cat.predict(X_ensemble)
    final_preds = (preds_xgb + preds_cat) / 2
    
    # --- PASSO 4: SALVAR RESULTADOS ---
    # Criando DataFrame para persistir no catálogo wk_...
    results_df = pd.DataFrame({
        'real': target.ravel(),
        'pred_ensemble': final_preds,
        'cluster_id': clusters
    })
    
    spark_df = spark.createDataFrame(results_df)
    # Salvando no seu esquema de logs que criamos antes
    spark_df.write.mode("overwrite").saveAsTable("sku_analytics_logs.ensemble_results")
    
    print("✅ Ensemble e Clustering concluídos e salvos no Delta!")

if __name__ == "__main__":
    train_complex_ensemble()