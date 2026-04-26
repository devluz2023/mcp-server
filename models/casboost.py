import mlflow
import mlflow.catboost
import optuna
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1. Inicialização do Spark
spark = SparkSession.builder \
    .appName("LogisticaQualidadeCompleto") \
    .getOrCreate()

# 2. Mock de dados e gravação na tabela "pedidos"
def preparar_ambiente():
    data = [
        (i, f"Transp_{i%5}", f"Motorista_{i%20}", f"Empresa_{i%10}", 
         float(i%50 + 1), float(i%100)/100, i%2)
        for i in range(1000)
    ]
    columns = ["id", "transportadora", "motorista", "empresa", "toneladas", "qualidade_hist", "target"]
    df = spark.createDataFrame(data, columns)
    
    # Simula a gravação na tabela no Lakehouse
    df.write.mode("overwrite").saveAsTable("pedidos_entrega")
    return df

df_spark = preparar_ambiente()

# 3. Feature Engineering via PySpark
# Calculamos a média de toneladas por empresa para identificar outliers de volume
df_features = df_spark.withColumn(
    "media_empresa", F.avg("toneladas").over(F.window("empresa"))
).withColumn(
    "tonelada_relativa", F.col("toneladas") / F.col("media_empresa")
)

# Converter para Pandas para o treino (CatBoost é local por padrão)
pdf = df_features.toPandas()
X = pdf.drop(['target', 'id', 'media_empresa'], axis=1)
y = pdf['target']
cat_features = ['transportadora', 'motorista', 'empresa']

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2)

# 4. Otimização com Optuna
def objective(trial):
    param = {
        'iterations': trial.suggest_int('iterations', 100, 300),
        'depth': trial.suggest_int('depth', 4, 8),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2),
        'loss_function': 'Logloss',
        'verbose': False
    }
    
    model = CatBoostClassifier(**param, cat_features=cat_features)
    model.fit(X_train, y_train)
    preds = model.predict(X_val)
    return accuracy_score(y_val, preds)

study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=15)

# 5. Registro no MLflow e Treino Final
mlflow.set_experiment("Pipeline_Qualidade_Logistica")

with mlflow.start_run():
    best_params = study.best_params
    final_model = CatBoostClassifier(**best_params, cat_features=cat_features)
    final_model.fit(X_train, y_train)
    
    # Logar parâmetros e o modelo
    mlflow.log_params(best_params)
    mlflow.catboost.log_model(final_model, "modelo_qualidade_entrega")
    
    print(f"Treinamento concluído. Melhor Acurácia: {study.best_value}")
    
    # Simular gravação de predições de volta na tabela Spark
    pdf['predicao'] = final_model.predict(X)
    df_result = spark.createDataFrame(pdf[['id', 'predicao']])
    df_result.write.mode("overwrite").saveAsTable("gold_predicoes_qualidade")
    print("Predições gravadas na tabela 'gold_predicoes_qualidade'")