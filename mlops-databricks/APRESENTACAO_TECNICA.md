# Apresentação Técnica: Arquitetura de Dados, Design de ML e MLOps
## Duração: 60 minutos | Foco: Engenheiros e Arquitetos

---

## AGENDA (1 hora)

| Tempo | Tópico | Duração |
|-------|--------|---------|
| 0:00 - 0:05 | Introdução Rápida | 5 min |
| 0:05 - 0:20 | Arquitetura de Dados (Lakehouse) | 15 min |
| 0:20 - 0:35 | Design de Machine Learning | 15 min |
| 0:35 - 0:50 | MLOps e Automação | 15 min |
| 0:50 - 1:00 | Demo Técnica + Q&A | 10 min |

---

# SLIDE 1: Introdução Rápida (0:00 - 0:05)

## Escopo Técnico

Vamos mergulhar em 3 pilares de um sistema ML moderno:

```
┌─────────────────────────────────────────────────────────┐
│  Dados                ML                 Operações      │
│  (Qualidade)          (Precisão)         (Confiabilidade) │
│                                                         │
│  ✓ Governança         ✓ Reproducibilidade  ✓ Automação │
│  ✓ Escalabilidade     ✓ Robustez           ✓ Monitoramento │
│  ✓ Versionamento      ✓ Eficiência         ✓ Rollback   │
└─────────────────────────────────────────────────────────┘
```

**Case**: Predição de preços de reservas (hotel-booking dataset, 40k+ registros)

---

# SLIDE 2: Arquitetura de Dados - Parte 1: O Lakehouse (0:05 - 0:20)

## Conceito: Por que Lakehouse?

### Problema Histórico:

```
Data Lake (≤ 2010):
├─ ✓ Armazena qualquer dado (schema-on-read)
├─ ✓ Barato
├─ ✓ Escalável
└─ ✗ Sem ACID, sem governança → "Data Swamp"

Data Warehouse (OLAP):
├─ ✓ ACID, índices
├─ ✓ Performance para analytics
├─ ✓ Governança
└─ ✗ Caro, rígido, schema-on-write

Lakehouse (2020+): Combina o melhor dos dois
├─ ✓ Dados tipo Lake (flexível, escalável)
├─ ✓ Garantias tipo Warehouse (ACID, governança)
├─ ✓ Delta Lake: Transações ACID em Parquet
└─ ✓ Unity Catalog: Governança + Linhagem de dados
```

### Arquitetura Lakehouse do Projeto:

```
┌──────────────────────────────────────────────────────────┐
│                    LAKEHOUSE (Databricks)                │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  STORAGE LAYER                                          │
│  ┌─────────────────────────────────────────────┐        │
│  │  Cloud Storage (S3/Azure Blob)              │        │
│  │  └─ Parquet Files (Columnar, Compressed)   │        │
│  │     └─ Delta Lake: _delta_log/ (ACID)      │        │
│  └─────────────────────────────────────────────┘        │
│                      ↑                                   │
│  COMPUTE LAYER                                          │
│  ┌─────────────────────────────────────────────┐        │
│  │  Apache Spark                               │        │
│  │  ├─ Distributed processing (1000+ cores)   │        │
│  │  ├─ Fault tolerance + Auto-scaling         │        │
│  │  └─ SQL + Python/Scala/R APIs              │        │
│  └─────────────────────────────────────────────┘        │
│                      ↑                                   │
│  METADATA LAYER                                         │
│  ┌─────────────────────────────────────────────┐        │
│  │  Unity Catalog                              │        │
│  │  ├─ Metastore (schemas, tables, columns)   │        │
│  │  ├─ Access Control (DAC + RBAC)            │        │
│  │  ├─ Data Lineage (provenance)              │        │
│  │  └─ Data Classification (PII tags)         │        │
│  └─────────────────────────────────────────────┘        │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### Comparação: Arquiteturas de Dados

```
TRADICIONAL (Data Warehouse)    LAKEHOUSE (Databricks)
─────────────────────────────    ─────────────────────────

ETL:
CSV → Extract → Transform        CSV → Spark Job → Delta
   → Load to WH                      (Auto-scaling)
   (8h batch)                        (Minutes)

Data Model:
Star schema, rigid               Flexible (Bronze→Silver→Gold)
Hard to change                   Easy to experiment

Analytics:
SQL warehouse                    SQL + ML + Notebooks
Complex BI tools                 Integrated platform

Governance:
Manual access control            Unity Catalog (automatic)
Hard to track lineage            Built-in provenance

Cost:
High compute $                   Pay per compute
Storage locked in                Storage separate (cheaper)
```

## Camadas de Dados no Projeto

### Layer 1: Bronze (Raw)

```
Source: CSV (data/booking.csv)
│
├─ Load: PySpark read_csv
│  └─ 40,000 rows × 20 columns
│  └─ Raw types: strings, nulls, weird formats
│
└─ Storage: Delta table
   └─ {catalog}.{schema}.hotel_booking_raw
   └─ Partitioned by: arrival_date
   └─ Z-order: booking_id (speedup lookups)
   
Retention: 90 days (cheap storage, for replay/debug)
```

**Dados Crus Exemplo:**

```
booking_id | date_of_reservation | arrival_date  | lead_time | average_price | ...
-----------|----------------------|---------------|-----------|---------------|-----
BK0000001  | 3/1/2018            | 3/15/2018     | 14        | 125.50       | ...
BK0000002  | 3/2/2018            | 2018-2-29 ??? | -5        | NULL         | ...  ← DIRTY!
BK0000003  | 3/3/2018            | 3/20/2018     | 17        | 285.75       | ...
```

### Layer 2: Silver (Processed)

```
Input: Bronze layer
│
├─ Transformations (Data Processor):
│  ├─ Fix bad dates (2018-2-29 → 3/1/2018)
│  ├─ Normalize column names (spaces/hyphens → underscores)
│  ├─ Fill nulls (strategy: median for numeric, mode for categorical)
│  ├─ Outlier detection (lead_time > 365 → flag)
│  ├─ Type conversion (strings → dates/numbers)
│  └─ Create derived features:
│     ├─ arrival_month = MONTH(arrival_date)
│     ├─ is_weekend = (day_of_week(arrival_date) in [6,7])
│     └─ days_stay = number_of_week_nights + number_of_weekend_nights
│
└─ Storage: Delta table (OPTIMIZED)
   └─ {catalog}.{schema}.hotel_booking
   └─ Partitioned by: year, month (for efficient queries)
   └─ Z-order: booking_id, arrival_date
   └─ Optimize: Run VACUUM (remove old versions)
   
Retention: 1 year (training data history)
Refresh: Daily (incremental append)
```

**Dados Processados:**

```
booking_id | arrival_date | lead_time | arrival_month | is_weekend | days_stay | average_price | ...
-----------|--------------|-----------|---------------|------------|-----------|---------------|-----
BK0000001  | 2018-03-15   | 14        | 3             | 1          | 5         | 125.50        | ...
BK0000002  | 2018-03-01   | 0         | 3             | 0          | 2         | 98.00         | ...  ← FIXED!
BK0000003  | 2018-03-20   | 17        | 3             | 1          | 7         | 285.75        | ...
```

### Layer 3: Gold (Curated)

```
Input: Silver layer (feature engineering)
│
├─ Aggregations:
│  ├─ Monthly avg_price by room_type
│  ├─ Weekly occupancy rates
│  └─ Seasonal patterns (by month)
│
├─ Feature Store:
│  └─ hotel_booking_price_preds (Feature Table)
│     ├─ Primary Key: booking_id
│     ├─ Features: 
│     │  ├─ predicted_price (from model)
│     │  ├─ lead_time_normalized (scaled 0-1)
│     │  └─ seasonality_factor (sin/cos encoding)
│     └─ Online Serving: Enabled (low-latency lookup)
│
└─ Storage: Delta tables (optimized for serving)
   └─ Multiple versions (can rollback)
   └─ SLA: Refresh <5 min
```

## Delta Lake: Por Que ACID em Data Lake?

### Problema: Sem ACID em Data Lakes

```
Scenario: 2 jobs writing simultaneously

Job A (insert 1000 rows)        Job B (insert 500 rows)
       ├─ Write part A1              ├─ Write part B1
       │                             │
       ├─ Write part A2        ← Job B reads A1+B1 (incomplete!)
       │                        → Creates corrupt state
       └─ Commit                └─ Commit

Result: Data corruption, consistency violated!
```

### Solução: Delta Lake ACID

```
Delta Lake usa Write-Ahead Log (_delta_log/):

┌─ _delta_log/
│  ├─ 00000000000000000000.json (Initial state)
│  ├─ 00000000000000000001.json (Job A: +1000 rows)
│  ├─ 00000000000000000002.json (Job B: +500 rows)
│  └─ ... (immutable, versioned)

Benefits:
├─ ACID Transactions: All-or-nothing writes
├─ Time Travel: SELECT * FROM table VERSION AS OF '2024-01-15'
├─ Rollback: RESTORE TABLE table TO VERSION 5
└─ Merge: UPDATE + DELETE in single atomic operation
```

**Exemplo Prático:**

```python
from delta.tables import DeltaTable

# Read current table
df = spark.read.delta("path/to/hotel_booking")

# Conditional update (safe, atomic)
deltaTable = DeltaTable.forPath(spark, "path/to/hotel_booking")
deltaTable.update(
    condition="booking_id = 'BK0000002'",
    set={"average_price": "98.00"}  # Fix bad value
)

# If anything fails mid-way: rollback automatically
# If succeeds: new version in _delta_log/

# Can revert if needed
spark.sql("RESTORE TABLE hotel_booking TO VERSION 5")
```

## Unity Catalog: Governança Centralizada

### Problema Sem UC:

```
Descentralized permissions:
├─ Dev Lake: Dev team tem acesso a tudo
├─ Prod Lake: ???
├─ PII data: Que está exposto?
├─ Lineage: De onde vem este dado?
└─ Compliance: Quem acessou quando?

Result: Data leaks, GDPR violations, chaos!
```

### Solução: Unity Catalog Arquitetura

```
┌────────────────────────────────────────────────────┐
│           UNITY CATALOG (Centralized)              │
├────────────────────────────────────────────────────┤
│                                                    │
│  Metastore (Root)                                 │
│  └─ Catalog: mlops_dev                           │
│     ├─ Schema: hotel_booking                      │
│     │  ├─ Table: hotel_booking (Bronze)          │
│     │  │  ├─ Column: booking_id (PII)            │
│     │  │  ├─ Column: average_price (public)      │
│     │  │  └─ Grants: OWNER=dataeng, SELECT=ds   │
│     │  │
│     │  └─ Table: hotel_booking (Silver)          │
│     │     └─ Grants: SELECT=all_teams            │
│     │
│     └─ Table: hotel_booking_price_preds (Gold)  │
│        ├─ Provenance: Computed from Silver       │
│        └─ Grants: SELECT=app, INSERT=ml_eng     │
│                                                    │
│  └─ Catalog: mlops_prd                           │
│     └─ [Similar structure, more restrictive]     │
│                                                    │
└────────────────────────────────────────────────────┘
```

### Access Control:

```
Privileges (Granular):
├─ SELECT: Read data
├─ CREATE: Create table
├─ MODIFY: ALTER table
├─ DELETE: DROP
└─ EXECUTE: Call functions

Roles (Predefined):
├─ OWNER: Full access
├─ EDITOR: SELECT, CREATE, MODIFY
├─ VIEWER: SELECT only
└─ NONE: No access

Example:
GRANT SELECT ON TABLE mlops_dev.hotel_booking TO GROUP data_scientists
GRANT MODIFY ON SCHEMA mlops_dev.hotel_booking TO GROUP data_engineers
```

### Data Classification & Masking:

```
Column Tags (Metadata):
├─ booking_id: {"tag": "PII", "pii_type": "identifier"}
├─ customer_email: {"tag": "PII", "pii_type": "email"}
└─ average_price: {"tag": "PUBLIC"}

Masking Policies (Automatic):
├─ IF tag=PII AND role=analyst:
│  └─ Show: booking_id → "***0001" (last 4 only)
└─ IF tag=PUBLIC:
   └─ Show: average_price → full value

Result: Same query, different data per user (automatic!)
```

---

# SLIDE 3: Design de Machine Learning - Parte 1 (0:20 - 0:35)

## Título: "Coração do Sistema: Design de ML"

### Visão Geral do Problema

```
┌─────────────────────────────────────────────────────────────┐
│                    ML PROBLEM STATEMENT                     │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│ 🎯 TASK: Regression (Prever preço médio de reserva)         │
│ 📊 DATA: 40k reservas históricas (18 meses)                 │
│ 🔍 FEATURES: 11 numéricas + 4 categóricas + engineered      │
│ 🎯 TARGET: average_price ($50-$500)                         │
│ 📈 METRICS: RMSE, MAE, R² (thresholds definidos)            │
│ 🚀 DEPLOYMENT: Real-time API (<100ms latency)              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Feature Engineering: De Raw para ML-Ready

#### Raw Features (Bronze Layer)
```
Numéricas (7):
├─ lead_time: 0-500 (dias de antecedência) ⭐⭐⭐
├─ number_of_adults: 1-4
├─ number_of_children: 0-2
├─ number_of_weekend_nights: 0-5
├─ number_of_week_nights: 0-7
├─ car_parking_space: 0-1 (binary)
└─ special_requests: 0-5

Categóricas (4):
├─ type_of_meal: Breakfast, Half Board, Full Board, All Inclusive
├─ room_type: Standard, Deluxe, Suite ⭐⭐
├─ arrival_month: 1-12 ⭐⭐
└─ market_segment_type: Aviation, Corporate, Leisure, etc.
```

#### Feature Engineering (Silver → Gold)
```
Transformações Aplicadas:
├─ Normalização: lead_time_normalized = lead_time / max(lead_time)
├─ Derivações: days_stay = week_nights + weekend_nights
├─ Cíclicas: seasonality_sin = sin(2π × arrival_month / 12)
│            seasonality_cos = cos(2π × arrival_month / 12)
├─ Business Logic: is_peak_season = arrival_month in [6,7,8]
└─ Ratios: weekend_ratio = weekend_nights / total_nights

Resultado: 15+ features otimizadas para ML
```

### Data Split: Temporal (Crítico para Time Series)

#### Por Que Temporal? (Não Random!)

```
❌ RANDOM SPLIT (PROBLEMA):
   ┌─────────────────────────────────────────────┐
   │ Time ─────────────────────────────────────> │
   │                                             │
   │ Train: [Jan, May, Sep, Dec] (misturado)   │
   │ Test:  [Mar, Jul, Nov, Apr] (misturado)   │
   │                                             │
   │ ❌ Modelo "vê" futuro durante treino       │
   │ ❌ Overfitting em padrões temporais        │
   └─────────────────────────────────────────────┘

✅ TEMPORAL SPLIT (CORRETO):
   ┌─────────────────────────────────────────────┐
   │ Time ─────────────────────────────────────> │
   │                                             │
   │ Train: [Jan.......Aug] (12 meses passado) │
   │ Test:  [Sep.......Oct] (1 mês futuro)     │
   │                                             │
   │ ✅ Treina passado, testa futuro            │
   │ ✅ Simula produção real                    │
   └─────────────────────────────────────────────┘
```

#### Implementação Técnica

```python
# DataLoader.split() - Temporal Split
def split(self, test_months=1, train_months=12, max_date=None):
    # Timeline: max_date ← test ← validation ← train
    
    train_query = f"""
    SELECT * FROM {self.table}
    WHERE arrival_date >= date_sub('{max_date}', {train_months + 2} MONTH)
    AND arrival_date < date_sub('{max_date}', {test_months + 1} MONTH)
    """
    
    test_query = f"""
    SELECT * FROM {self.table}
    WHERE arrival_date >= date_sub('{max_date}', {test_months} MONTH)
    AND arrival_date < '{max_date}'
    """
    
    return spark.sql(train_query), spark.sql(test_query)
```

### Algoritmo: LightGBM (Por Que?)

#### Comparação de Algoritmos

```
┌────────────────┬──────────────┬─────────────┬──────────────┬─────────────┐
│ Algorithm      │ Speed        │ Accuracy    │ Categorical  │ Complexity  │
├────────────────┼──────────────┼─────────────┼──────────────┼─────────────┤
│ Linear Reg     │ ⚡⚡⚡        │ ⭐⭐         │ ❌           │ 🔧           │
│ Decision Tree  │ ⚡⚡          │ ⭐⭐⭐        │ ✅           │ 🔧🔧         │
│ Random Forest  │ ⚡            │ ⭐⭐⭐⭐       │ ✅           │ 🔧🔧🔧       │
│ LightGBM ⭐    │ ⚡⚡⚡        │ ⭐⭐⭐⭐⭐      │ ✅ Native    │ 🔧🔧         │
│ XGBoost        │ ⚡⚡          │ ⭐⭐⭐⭐⭐      │ ❌           │ 🔧🔧🔧       │
│ Neural Net     │ ⚡            │ ⭐⭐⭐⭐       │ ❌           │ 🔧🔧🔧🔧     │
└────────────────┴──────────────┴─────────────┴──────────────┴─────────────┘

LightGBM Vantagens:
├─ 10x mais rápido que XGBoost (fewer trees)
├─ Categorical features nativas (sem encoding manual)
├─ GPU support (treino em segundos)
├─ Feature importance built-in
└─ Campeão em competições (Kaggle, Microsoft)
```

#### LightGBM Architecture

```
Input: X_train (40k × 15 features), y_train (prices)

Pipeline:
├─ Categorical Encoding (automático):
│  ├─ room_type: Standard→0, Deluxe→1, Suite→2
│  └─ meal_type: Breakfast→0, HB→1, FB→2, All→3
│
└─ Ensemble Learning:
   ├─ Tree 1: Split on lead_time (< 30 days?)
   ├─ Tree 2: Split on room_type, then arrival_month
   ├─ Tree 3: Split on days_stay (> 3 nights?)
   └─ ... (200 trees total)
   
   Prediction = Σ(learning_rate × tree_prediction)
              = 0.05 × (150 + 180 + 165 + ...) 
              ≈ $287.50

Hyperparameters (Otimizados):
├─ learning_rate: 0.05 (trade-off speed vs. overfitting)
├─ n_estimators: 200 (trees)
├─ max_depth: 3 (prevents overfitting)
├─ num_leaves: 8 (max leaves per tree)
└─ min_data_in_leaf: 20 (prevents noise)
```

### Métricas de Avaliação (Regression)

#### Métricas Principais

```python
# Após treino
y_pred = model.predict(X_test)

# 1. RMSE (Root Mean Squared Error)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
# Penaliza erros grandes (squared)
# Ex: RMSE=12.50 → erro médio $12.50
# Target: < $15 (5% do preço médio)

# 2. MAE (Mean Absolute Error)
mae = mean_absolute_error(y_test, y_pred)
# Robusto a outliers
# Ex: MAE=9.30 → erro médio $9.30
# Alert threshold: > $30

# 3. R² (Coeficiente de Determinação)
r2 = r2_score(y_test, y_pred)
# Fração da variância explicada
# R²=0.88 → modelo explica 88% da variação
# Target: > 0.85

# 4. MAPE (Mean Absolute Percentage Error)
mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
# Mais interpretável para negócio
# MAPE=7.2% → erro médio 7.2%
```

#### Resultados do Modelo

```
┌─────────────────────────────────────────────────┐
│                MODEL PERFORMANCE                 │
├─────────────────────────────────────────────────┤
│ Métrica          | Valor | Target | Status       │
├──────────────────┼───────┼────────┼──────────────┤
│ RMSE            | 12.50 | <15   | ✅ PASS      │
│ MAE             | 9.30  | <30   | ✅ PASS      │
│ R²              | 0.88  | >0.85 | ✅ PASS      │
│ MAPE            | 7.2%  | <10%  | ✅ PASS      │
└─────────────────────────────────────────────────┘

Interpretando:
├─ RMSE vs MAE: Razão 1.34 → poucos outliers
├─ R² alto: Modelo captura bem a variância
├─ MAPE baixo: Impacto negócio aceitável
└─ Pronto para produção!
```

### Feature Importance (Interpretabilidade)

#### Top Features (LightGBM Built-in)

```
Ranking de Importância:
├─ lead_time: 0.35 (35% dos splits)
├─ arrival_month: 0.22 (sazonalidade forte)
├─ room_type: 0.18 (tipo quarto impacta preço)
├─ days_stay: 0.12 (duração da estadia)
├─ special_requests: 0.08 (pouco impacto)
└─ other: 0.05

Visualização:
┌────────────────────────────┐
│ Feature Importance          │
├────────────────────────────┤
│ lead_time     ████████████ │ 35%
│ arrival_month ███████      │ 22%
│ room_type     ██████       │ 18%
│ days_stay     ████         │ 12%
└────────────────────────────┘
```

#### Insights de Negócio

```
lead_time alto → Reservas antecipadas têm desconto
arrival_month → Pico em verão (junho-agosto)
room_type → Deluxe/Suite premium pricing
days_stay → Estadias longas = preços mais altos

Por que importa?
├─ Valida se features fazem sentido de negócio
├─ Detecta data leakage (features "futuras")
├─ Suporte para decisões (ex.: focar em lead_time)
└─ Compliance (GDPR: explicar decisões)
```

### Talking Points (Para Apresentação)

- **Por que regressão?** Preço contínuo, não classificação binária.
- **LightGBM vs. outros?** Melhor trade-off speed/accuracy para tabulares.
- **Split temporal crítico**: Evita overconfidence (modelo "vê" futuro).
- **Feature engineering = 80% do trabalho**: Features ruins = modelo ruim.
- **Métricas múltiplas**: Cada uma conta uma parte da história.
- **Interpretabilidade**: Não é black-box; podemos explicar previsões.

---

**Próximo: MLOps e Automação**

---

# SLIDE 4: MLOps e Automação (0:35 - 0:50)

## MLOps Architecture (End-to-End)

```
┌─────────────────────────────────────────────────────────────┐
│              MLOps Pipeline (Databricks)                    │
└─────────────────────────────────────────────────────────────┘

[Manual Trigger / Scheduled Job]
           ↓
┌────────────────────────────────────────────┐
│ STAGE 1: DATA PREPARATION                  │
├────────────────────────────────────────────┤
│ Task: preprocess_data.py                   │
│ ├─ Input: data/booking.csv (raw)           │
│ ├─ Process: DataProcessor.preprocess()     │
│ │  ├─ Fix dates, normalize columns         │
│ │  ├─ Handle nulls, feature derivation     │
│ │  └─ Store in Silver layer                │
│ ├─ Output: {catalog}.{schema}.hotel_booking│
│ ├─ Time: ~5 minutes                        │
│ └─ Depends: None (independent)             │
└────────────────────────────────────────────┘
           ↓
┌────────────────────────────────────────────┐
│ STAGE 2: TRAINING + EVALUATION             │
├────────────────────────────────────────────┤
│ Task: train_register_model.py              │
│ ├─ Input: Silver layer (split temporal)    │
│ ├─ Process:                                │
│ │  ├─ DataLoader.split(test=1m, train=12m)│
│ │  ├─ LightGBMModel.train(X, y)            │
│ │  ├─ Evaluate metrics (RMSE, MAE, R²)     │
│ │  ├─ Log to MLflow                        │
│ │  └─ Register in Unity Catalog            │
│ ├─ Output: Model {catalog}.{schema}.hb_v42│
│ ├─ Time: ~10 minutes (includes tuning)     │
│ └─ Depends: Stage 1 complete               │
└────────────────────────────────────────────┘
           ↓
┌────────────────────────────────────────────┐
│ STAGE 3: VALIDATION + PROMOTION            │
├────────────────────────────────────────────┤
│ Task: Automated checks (in script)         │
│ ├─ Check 1: New RMSE < Previous RMSE?      │
│ ├─ Check 2: R² > 0.85 threshold?           │
│ ├─ Check 3: No degradation in subgroups?   │
│ │  (RMSE by room_type, arrival_month)      │
│ ├─ Check 4: Features not drifted?          │
│ │                                           │
│ ├─ If all pass:                            │
│ │  └─ Alias 'latest-model' → new model    │
│ ├─ If any fail:                            │
│ │  └─ Keep old model, alert engineer       │
│ └─ Time: <1 minute                         │
└────────────────────────────────────────────┘
           ↓
┌────────────────────────────────────────────┐
│ STAGE 4: SERVING (Online Predictions)      │
├────────────────────────────────────────────┤
│ Task: Endpoint updated automatically       │
│ ├─ Models endpoints.create() with v42      │
│ ├─ Feature Store synced                    │
│ ├─ Old endpoint (version) still available  │
│ ├─ API ready: /api/v2/models/.../invoke   │
│ └─ Time: <2 minutes                        │
└────────────────────────────────────────────┘
           ↓
┌────────────────────────────────────────────┐
│ CONTINUOUS MONITORING                      │
├────────────────────────────────────────────┤
│ ├─ Prediction Logging:                     │
│ │  └─ Every request logged to table        │
│ │     (timestamp, input features, output)  │
│ │                                           │
│ ├─ Drift Detection (Daily):                │
│ │  ├─ Data drift: Compare feature dist.    │
│ │  │  (KS test: p < 0.05 = significant)    │
│ │  ├─ Prediction drift: Are predictions    │
│ │  │  shifting? (trend analysis)           │
│ │  └─ Label drift: If ground truth avail.  │
│ │     (is actual price changing?)          │
│ │                                           │
│ ├─ Performance Metrics:                    │
│ │  ├─ MAE: |actual - predicted|            │
│ │  ├─ Latency: Response time (target <100m)│
│ │  ├─ Throughput: Requests/sec             │
│ │  └─ Error rate: Exceptions/failures      │
│ │                                           │
│ ├─ Alerts (Triggered):                     │
│ │  ├─ MAE > 30: Email alert                │
│ │  ├─ Latency > 200ms: PagerDuty alert     │
│ │  ├─ Data drift detected: Investigate     │
│ │  └─ Endpoint down: Auto-rollback          │
│ │                                           │
│ └─ Feedback Loop:                          │
│    └─ If drift/perf degrade → Trigger      │
│       re-training (Stage 1-2)              │
└────────────────────────────────────────────┘
```

## Job Definition (Databricks Asset Bundles)

### resources/ml_pipeline.yml:

```yaml
resources:
  jobs:
    ml-pipeline:
      name: hotel-booking-ml-pipeline
      
      schedule:
        quartz_cron_expression: "0 0 6 ? * MON"  # Monday 6am UTC
        pause_status: PAUSED                     # Initially paused
      
      tasks:
        
        # TASK 1: Preprocessing
        - task_key: preprocessing
          spark_python_task:
            python_file: ../scripts/preprocess_data.py
            parameters:
              - "common"
              - "--root_path"
              - ${workspace.root_path}
              - "--env"
              - ${bundle.target}          # dev, acc, prd
          timeout_seconds: 900              # 15 min max
        
        # TASK 2: Training (depends on Task 1)
        - task_key: train_model
          depends_on:
            - task_key: preprocessing
          spark_python_task:
            python_file: ../scripts/train_register_model.py
            parameters:
              - "train_deploy_model"
              - "--root_path"
              - ${workspace.root_path}
              - "--env"
              - ${bundle.target}
              - "--run_id"
              - "{{job.run_id}}"           # Job run ID for tracking
          timeout_seconds: 1200             # 20 min max
        
        # TASK 3: Model evaluation (auto validation)
        # [Embedded in train_register_model.py]
        
        # Task 4: Serving updated in CI/CD
        # [Can be manual or automated]

      environments:
        - environment_key: default
          spec:
            environment_version: "4"
            dependencies:
              - ../dist/*.whl               # Built package
```

### Deploy Command:

```bash
# Build package
uv build                                    # Generates .whl

# Deploy to dev
databricks bundle deploy --target dev      # Uploads to workspace

# Deploy to production
databricks bundle deploy --target prd      # With validation checks

# Run manually
databricks bundle run ml-pipeline --target prd
```

## MLflow Experiment Tracking

### What Gets Logged:

```python
# In train_register_model.py

with mlflow.start_run(experiment_name="/Shared/hotel-booking-training") as run:
    
    # 1. Parameters (hyperparameters)
    mlflow.log_params({
        "learning_rate": 0.05,
        "n_estimators": 200,
        "max_depth": 3,
        "train_months": 12,
        "test_months": 1
    })
    
    # 2. Metrics (evaluation results)
    mlflow.log_metrics({
        "rmse": 12.50,
        "mae": 9.30,
        "r2": 0.88,
        "mape": 7.2,
        "training_time_sec": 145
    })
    
    # 3. Model (serialized)
    mlflow.sklearn.log_model(
        model.pipeline,
        artifact_path="model",
        input_example=X_train.iloc[:5],
        signature=infer_signature(X_train, y_train)
    )
    
    # 4. Artifacts (files)
    mlflow.log_artifact(
        "plots/actual_vs_predicted.png",
        artifact_path="plots"
    )
    mlflow.log_artifact(
        "plots/feature_importance.png"
    )
    
    # 5. Tags (metadata)
    mlflow.set_tags({
        "git_sha": "abc123def",
        "branch": "main",
        "run_id": "{{job.run_id}}",
        "environment": "prd",
        "model_type": "lightgbm_regression"
    })
    
    run_id = run.info.run_id
    print(f"Run ID: {run_id}")
```

### MLflow UI View:

```
Experiment: /Shared/hotel-booking-training

┌─────────────────────────────────────────────────┐
│ Run History                                     │
├─────────────────────────────────────────────────┤
│ Run        Date        RMSE  MAE   R²   Status │
├─────────────────────────────────────────────────┤
│ abc123     2024-04-20  12.5  9.3   0.88 ✓ (latest)
│ abc122     2024-04-13  13.2  10.1  0.85 ✓
│ abc121     2024-04-06  15.8  11.7  0.82 ✗ (regression)
│ abc120     2024-03-30  12.8  9.5   0.87 ✓
└─────────────────────────────────────────────────┘

Click on run → Details:
├─ Parameters tab: learning_rate, n_estimators, ...
├─ Metrics tab: RMSE, MAE, R², ... (with time series)
├─ Artifacts tab: model/, plots/
└─ Register Model → Promote to Production
```

## Feature Store for Consistent Inference

### The Problem:

```
Without Feature Store:

TRAINING:
├─ Data scientist creates features manually
├─ Saves features in notebook
├─ Trains model: features = [f1, f2, ...]
└─ Metrics: Good!

SERVING (3 months later):
├─ Different engineer creates features "again"
├─ But implementation slightly different!
│  (different null handling, rounding, etc.)
├─ Model gets new features: features ≠ [f1, f2, ...]
└─ Predictions are WRONG! ← Production bug
```

### Solution: Feature Store

```python
# DURING TRAINING:

from databricks.feature_engineering import FeatureEngineeringClient

fe = FeatureEngineeringClient()

# Create feature table
features_df = spark.createDataFrame([
    ("BK0000001", 287.50, 0.33, 0.95),
    ("BK0000002", 125.50, 0.47, 0.42),
    # ...
], ["booking_id", "predicted_price", "lead_time_norm", "seasonality"])

fe.create_table(
    name=f"{cfg.catalog}.{cfg.schema}.hotel_booking_price_preds",
    primary_keys=["booking_id"],
    df=features_df,
    description="Hotel Booking Price Predictions"
)

# Train model using these features
model = LightGBMModel(config)
model.train(X_train, y_train)

# Register model + features together
mlflow.log_model(model, "model")  # Points to feature table


# DURING SERVING:

from databricks.feature_engineering import FeatureLookup

# Create spec for online serving
fe.create_feature_lookup_table(
    spec_name=f"{cfg.catalog}.{cfg.schema}.return_hb_prices",
    table_name=f"{cfg.catalog}.{cfg.schema}.hotel_booking_price_preds",
    lookup_key="booking_id",
    feature_names=["predicted_price", "lead_time_norm"]
)

# In API:
@app.post("/predict")
def predict(booking_id: str):
    # Lookup features (CONSISTENT with training!)
    features = fe.get_feature_lookup_table(
        spec_name="...",
        lookup_key={"booking_id": booking_id}
    )
    
    # Predict using same features
    pred = model.predict(features)
    return {"predicted_price": pred}
```

## Monitoring & Drift Detection

### Lakehouse Monitoring Setup:

```python
# In refresh_monitor.py (ran periodically)

from databricks.sdk.service.compute import Policy

# Monitor inference table
monitor = ml.MonitorDefinition(
    table_name=f"{catalog}.{schema}.inference_table",
    primary_key="booking_id",
    timestamp_col="prediction_timestamp"
)

# Define baseline (reference for comparison)
monitor.baseline_table_name = f"{catalog}.{schema}.hotel_booking_clean"

# Add metrics
monitor.add_metric(
    "prediction_distribution",
    type="data_distribution_drift",
    features=["average_price"]  # Watch for price distribution changes
)

monitor.add_metric(
    "input_data_drift",
    type="data_distribution_drift",
    features=["lead_time", "arrival_month", "room_type"]
)

monitor.add_metric(
    "prediction_latency",
    type="performance",
    condition="latency_ms > 100"  # Alert if slow
)

# Create alerts
monitor.add_alert(
    metric_name="prediction_distribution",
    threshold=0.05,  # p-value < 0.05 = significant drift
    action="EMAIL",
    recipients=["maria@cauchy.io"]
)
```

### Drift Detection (Statistical):

```
Scenario: Monitoring lead_time feature

BASELINE (Training Data):
lead_time distribution: 
  mean: 20 days, std: 12, range: [0-180]

CURRENT (Last 7 days of predictions):
lead_time distribution:
  mean: 45 days, std: 25, range: [0-320]

Drift Test (Kolmogorov-Smirnov):
├─ Compare empirical CDFs
├─ Calculate KS statistic: 0.18
├─ p-value: 0.002 (< 0.05 threshold)
└─ Conclusion: SIGNIFICANT DRIFT DETECTED!

Action:
├─ Alert: "Data drift detected in lead_time"
├─ Reason: More advance bookings recently (post-Covid trends?)
├─ Recommendation: Re-train model (distribution changed)
└─ Human investigates: Market changed? New marketing campaign?
```

---

# SLIDE 5: Demo Técnica + Q&A (0:50 - 1:00)

## Demo 1: Explorando Delta Lake (2 min)

```python
# In Databricks Notebook

# 1. Read Delta table with time travel
df = spark.read.format("delta")\
    .option("versionAsOf", 5)\
    .load("/path/to/hotel_booking")

# 2. Check history
spark.sql("DESCRIBE HISTORY delta.`/path/to/hotel_booking`").show()

# Output:
# +---------+--------+---------+----------+-------+----------+--+
# |version  |timestamp|operation|user_id   |changes| ...       |
# +---------+--------+---------+----------+-------+----------+--+
# |10       |2024-04-20|WRITE    |user123   |+1000  | INSERT... |
# |9        |2024-04-19|DELETE   |user456   |-50    | WHERE ... |
# |8        |2024-04-18|MERGE    |user123   |+200   | ON ...    |
# +---------+--------+---------+----------+-------+----------+--+

# 3. Rollback if needed
spark.sql("RESTORE TABLE delta.`/path` TO VERSION 8")

# 4. Query metadata
spark.sql(f"""
SELECT COUNT(*) FROM {catalog}.{schema}.hotel_booking
WHERE arrival_date >= '2024-01-01'
""").show()
```

## Demo 2: MLflow Tracking (2 min)

```python
# Execute from notebook

import mlflow
mlflow.set_experiment("/Shared/hotel-booking-training")

with mlflow.start_run():
    # Train model
    model = LightGBMModel(config)
    model.train(X_train, y_train)
    
    # Log everything
    mlflow.log_params({"learning_rate": 0.05, "n_estimators": 200})
    mlflow.log_metrics({"rmse": 12.5, "mae": 9.3, "r2": 0.88})
    mlflow.sklearn.log_model(model.pipeline, "model")
    
    print(f"Run ID: {mlflow.active_run().info.run_id}")

# Open MLflow UI
# databricks-workspace.com/experiments/123/runs/abc123
```

## Demo 3: Feature Store Lookup (2 min)

```python
# Query feature table

from databricks.feature_engineering import FeatureEngineeringClient

fe = FeatureEngineeringClient()

# Get features for specific booking
features = fe.read_table(
    name=f"{catalog}.{schema}.hotel_booking_price_preds",
    as_pandas=True
).query("booking_id == 'BK0000123'")

print(features)
# Output:
#   booking_id predicted_price lead_time_norm seasonality
# 0 BK0000123           287.50           0.33        0.95
```

## Demo 4: Monitoring Dashboard (2 min)

```
Open: Databricks SQL → Dashboards → hotel-booking-monitor

Shows:
├─ [Card] Daily Predictions: 2,847
├─ [Card] MAE (7-day trend): 9.2$ → 9.8$ → 8.9$ (stable)
├─ [Card] Data Drift Alert: lead_time KS=0.18, p=0.002 ⚠️
├─ [Card] Latency P95: 76ms (target <100ms) ✓
└─ [Alert] Drift detected in lead_time - investigate
```

## Q&A

### Q1: How to handle concept drift (model gets old)?

A: Multiple strategies:
```
1. Automatic re-training (scheduled weekly)
   └─ Drift detected → Trigger job (automatic)

2. Online learning
   └─ Each new prediction updates model incrementally
   └─ More complex, but handles gradual drift

3. Ensemble of models
   └─ Keep multiple versions, vote on prediction
   └─ Mitigates if 1 model drifts

4. Monitoring + Manual intervention
   └─ Alert engineer if drift detected
   └─ Engineer can retrain with new data/features
```

### Q2: How to avoid leaking future information?

A: Temporal split + feature design:
```
✓ Correct:
├─ Split: train on past, test on future
├─ Features: Only use data available at prediction time
│  └─ lead_time (known at booking)
│  └─ seasonality (known in advance)
└─ No "ground truth" features in input!

✗ Wrong:
├─ Random split (mixes past/future)
├─ Features like "was_cancelled" (known after, not at booking time)
└─ Using previous month prices (future target info)
```

### Q3: How to scale to billions of rows?

A: Spark + Delta handles:
```
Spark Distribution:
├─ Data partitioned across 1000+ nodes
├─ Queries parallelized
├─ Delta compression (80% reduction typical)

Feature Store:
├─ Indexes on primary keys (fast lookups)
├─ Online serving via API (not full table scan)
├─ Caching for hot features

Tuning:
├─ Z-order optimization (spatial clustering)
├─ VACUUM old versions (free storage)
├─ Parallel training (Ray Tune)
```

### Q4: Cost of running this?

A:
```
Databricks pricing (~$0.40 per DBU-hour):

Development:
├─ Notebook clusters: 4 DBU × 2h/day × 22 days = ~$70/month
├─ SQL queries: 2 DBU × 1h/day × 22 days = ~$18/month
└─ Total dev: ~$100/month

Production:
├─ Job cluster (weekly retrain): 8 DBU × 0.5h = ~$2/week = ~$9/month
├─ Model serving (persistent): 4 DBU × 24h × 30 = ~$1,152/month
└─ Monitoring queries: 1 DBU × 2h/day × 30 = ~$24/month
└─ Total prd: ~$1,200/month (mostly serving)

Alternative (cheaper serving):
├─ Deploy model to separate container (AWS SageMaker, etc.)
├─ Only use Databricks for training/monitoring
└─ Serving cost ↓ 80%
```

### Q5: How secure are the data?

A: Unity Catalog + Encryption:
```
Access Control:
├─ Role-based (RBAC) + Attribute-based (ABAC)
├─ Column-level masking (PII automatic hide)
├─ Row-level security (users see different data)

Encryption:
├─ At-rest: AES-256 (AWS/Azure managed keys)
├─ In-transit: TLS 1.2+
├─ Databricks keys or BYOK (bring your own key)

Audit:
├─ Every read/write logged
├─ Who accessed which table, when
├─ Query history retained (compliance)

Compliance:
├─ GDPR: Data deletion (right to be forgotten)
├─ HIPAA: Encryption + audit trails
├─ SOC 2: Regular third-party audits
```

---

## RESUMO TÉCNICO (1 página)

### 1. Arquitetura de Dados
- **Lakehouse**: Combina Lake (scalability) + Warehouse (ACID)
- **Delta Lake**: Transaction log (_delta_log/) garante ACID
- **Camadas**: Bronze (raw) → Silver (clean) → Gold (curated)
- **Unity Catalog**: Governança centralizada (RBAC, linhagem, PII masking)

### 2. Design de ML
- **Problema**: Regressão (predizer average_price)
- **Features**: 11 numéricas + categóricas + engineered
- **Algoritmo**: LightGBM (rápido, acurado, interpretável)
- **Split**: Temporal (evita data leakage)
- **Métricas**: RMSE, MAE, R², MAPE

### 3. MLOps
- **Pipeline**: 4 stages (preprocess → train → validate → serve)
- **Automação**: Databricks Asset Bundles (jobs agendados)
- **Tracking**: MLflow (params, metrics, artifacts, model registry)
- **Feature Store**: Consistent features (train ↔ serve)
- **Monitoramento**: Drift detection (KS test), alerts, feedback loops
- **Governança**: Git-based (infrastructure-as-code), versioned

---

**Fim da Apresentação Técnica**
