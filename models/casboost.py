# ============================================
# CASBOOST - PIPELINE COMPLETO
# ============================================

import mlflow
import mlflow.catboost
import optuna
import pandas as pd

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.window import Window

from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# ============================================
# 1. SPARK
# ============================================
spark = SparkSession.builder.getOrCreate()

# ============================================
# 2. MOCK DE DADOS (simula lake)
# ============================================
def preparar_ambiente():
    data = [
        (i, f"Transp_{i%5}", f"Motorista_{i%20}", f"Empresa_{i%10}", 
         float(i%50 + 1), float(i%100)/100, i%2)
        for i in range(1000)
    ]

    columns = [
        "id", "transportadora", "motorista", "empresa",
        "toneladas", "qualidade_hist", "target"
    ]

    df = spark.createDataFrame(data, columns)

    # salva no lake
    df.write.mode("overwrite").saveAsTable("pedidos_entrega")

    return df


df_spark = preparar_ambiente()

# ============================================
# 3. FEATURE ENGINEERING (CORRETO)
# ============================================

window_spec = Window.partitionBy("empresa")

df_features = df_spark.withColumn(
    "media_empresa",
    F.avg("toneladas").over(window_spec)
).withColumn(
    "tonelada_relativa",
    F.col("toneladas") / F.col("media_empresa")
)

# evitar recomputação
df_features = df_features.cache()

# ============================================
# 4. AMOSTRAGEM (EVITA TRAVAR)
# ============================================
df_sample = df_features.limit(20000)

# ============================================
# 5. PARA PANDAS
# ============================================
pdf = df_sample.toPandas()

# ============================================
# 6. PREPARAÇÃO
# ============================================

X = pdf.drop(['target', 'id', 'media_empresa'], axis=1)
y = pdf['target']

cat_features = ['transportadora', 'motorista', 'empresa']

# garantir string
for col in cat_features:
    if col in X.columns:
        X[col] = X[col].astype(str)

X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ============================================
# 7. OPTUNA
# ============================================
def objective(trial):
    params = {
        'iterations': trial.suggest_int('iterations', 100, 300),
        'depth': trial.suggest_int('depth', 4, 8),
        'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.2),
        'loss_function': 'Logloss',
        'verbose': False
    }

    model = CatBoostClassifier(**params, cat_features=cat_features)
    model.fit(X_train, y_train)

    preds = model.predict(X_val)

    return accuracy_score(y_val, preds)


study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=10)

# ============================================
# 8. MLFLOW
# ============================================

mlflow.set_experiment("/Users/fabio.jdluz@gmail.com/casboost_pipeline")

with mlflow.start_run():

    best_params = study.best_params

    final_model = CatBoostClassifier(
        **best_params,
        cat_features=cat_features
    )

    final_model.fit(X_train, y_train)

    preds = final_model.predict(X_val)
    acc = accuracy_score(y_val, preds)

    mlflow.log_params(best_params)
    mlflow.log_metric("accuracy", acc)

    mlflow.catboost.log_model(
        final_model,
        "modelo_qualidade_entrega"
    )

    print(f"✅ Melhor acurácia: {acc}")

# ============================================
# 9. SALVAR RESULTADOS NO LAKE
# ============================================

pdf['predicao'] = final_model.predict(X)

df_result = spark.createDataFrame(
    pdf[['id', 'predicao']]
)

df_result.write.mode("overwrite") \
    .saveAsTable("gold_predicoes_qualidade")

print("✅ Predições salvas na tabela gold_predicoes_qualidade")