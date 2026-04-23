# Apresentação: MLOps com Databricks - Hotel Booking
## Duração: 60 minutos

---

## AGENDA (1 hora)

| Tempo | Tópico | Duração |
|-------|--------|---------|
| 0:00 - 0:05 | Abertura e Contexto | 5 min |
| 0:05 - 0:15 | O Problema de Negócio | 10 min |
| 0:15 - 0:25 | Arquitetura de Dados (Lakehouse) | 10 min |
| 0:25 - 0:35 | Design de Machine Learning | 10 min |
| 0:35 - 0:45 | MLOps e Pipeline de Produção | 10 min |
| 0:45 - 0:55 | Demo Prática / Walkthrough | 10 min |
| 0:55 - 1:00 | Próximos Passos e Q&A | 5 min |

---

# SLIDE 1: Abertura e Contexto (0:00 - 0:05)

## Título
**"MLOps com Databricks: Da Experimentação à Produção"**  
Baseado no livro O'Reilly "MLOps with Databricks"

### Talking Points:
- Bem-vindos! Essa apresentação aborda como operacionalizar Machine Learning em escala.
- Vamos usar um caso real: **predição de preços de reservas de hotéis**.
- Foco: Como ir de um notebook de data science para um sistema pronto para produção.
- Stack: Databricks, Delta Lake, MLflow, Feature Store, e MLOps automation.

### Visão Geral Rápida:
- **Problema**: Otimizar precificação dinâmica em rede hoteleira.
- **Solução**: Pipeline MLOps end-to-end com monitoring contínuo.
- **Resultado**: Aumento estimado de 5-10% em receita via ML.

---

# SLIDE 2: O Problema de Negócio (0:05 - 0:15)

## Título: "Por que MLOps Importa?"

### Contexto de Negócio:
```
Rede Hoteleira enfrenta:
├─ Precificação Manual → Lenta, inconsistente, deixa dinheiro na mesa
├─ Falta de Dados Estruturados → Decisões baseadas em intuição
├─ Sem Feedback Loop → Erros se repetem semana após semana
└─ Compliance Risk → Sem auditoria de decisões
```

### Oportunidade com ML:
- **Problema a Resolver**: Prever `average_price` (preço médio) para cada reserva baseado em features como:
  - `number_of_adults`, `number_of_children`, `lead_time`
  - `type_of_meal`, `room_type`, `arrival_month`
  
### Impacto de Negócio:
```
SEM ML:
├─ Margem média: 15%
├─ Overbooking: 5% de reservas perdidas
└─ Time de pricing: 2 pessoas, 20h/semana em análise manual

COM ML:
├─ Margem média: 20-22% (precificação dinâmica otimizada)
├─ Overbooking: Reduzido para <1% (previsões mais precisas)
└─ Time de pricing: 1 pessoa, 5h/semana (automação)

ROI: +5-10% em receita, -75% em tempo de análise
```

### Talking Points:
- Dados: Histórico de 40k+ reservas com preços, features do hóspede e da reserva.
- Objetivo: Modelo que prediz preço com ±5% de margem de erro.
- Desafio: Dados mudam (sazonalidade, eventos, competição). Modelo precisa re-treinar regularmente.
- Solução: MLOps automatiza isso, monitorando drift e re-treinando semanalmente.

---

# SLIDE 3: Arquitetura de Dados - Lakehouse (0:15 - 0:25)

## Título: "Fundação: Lakehouse com Delta Lake"

### O que é um Lakehouse?
```
Combina o melhor de Data Lakes + Data Warehouses:
├─ Data Lake (flexibilidade): Qualquer dado, qualquer formato
├─ + Data Warehouse (performance/governança): ACID, índices, controle de acesso
└─ = Lakehouse: Flexibilidade + Confiabilidade
```

### Camadas de Dados:

#### 1. Bronze Layer (Raw)
```
Dados brutos ingeridos conforme chegam:
├─ Origem: CSVs, APIs, Kafka, bancos legados
├─ Formato: Delta tables para versionamento
└─ Exemplo: Tabela `hotel_booking_raw` com 40k registros
```

#### 2. Silver Layer (Processed)
```
Dados limpos e transformados:
├─ Operações: 
│  ├─ Corrigir datas inválidas (2018-2-29 → 3/1/2018)
│  ├─ Normalizar colunas (espaços/hífens)
│  ├─ Criar features derivadas (arrival_month = reservation_date + lead_time)
│  └─ Remover duplicatas, outliers óbvios
├─ Armazenamento: `mlops_dev.hotel_booking.hotel_booking` (Delta otimizado)
└─ Performance: 1-5M registros, queries <1s
```

#### 3. Gold Layer (Curated)
```
Dados prontos para ML/Analytics:
├─ Inclui: Features engenheiradas, agregações, e Feature Store
├─ Consumidores: Modelos, dashboards, relatórios
└─ Garantias: Qualidade assegurada, SLA de refresh
```

### Governança com Unity Catalog:

```
Estrutura por Ambiente:
├─ mlops_dev
│  └─ hotel_booking
│     ├─ hotel_booking (tabela de treinamento)
│     ├─ hotel_booking_price_preds (feature store)
│     └─ ... [outros dados]
├─ mlops_acc
│  └─ hotel_booking (replica com dados de produção, sem PII)
└─ mlops_prd
   └─ hotel_booking (dados reais, máxima segurança)

Controle de Acesso:
├─ Data Engineers: SELECT, CREATE em Silver
├─ Data Scientists: SELECT em Silver, CREATE em Gold
├─ ML Engineers: SELECT em Gold, EXECUTE endpoints
└─ Auditoria: Todos os acessos logados
```

### Diagram Visual (ASCII):
```
[CSV] → [Bronze] → [Silver] → [Gold] → [Feature Store]
         (Raw)     (Clean)    (Curated)  (ML Ready)
           ↓         ↓          ↓           ↓
       [Delta]    [Delta]    [Delta]    [FS Tables]
         (14d)      (1y)       (2y)      (Online)

Governance: Unity Catalog rastreia TUDO
├─ Linhagem: Qual tabela vem de qual
├─ Permissões: Quem acessa o quê
└─ Auditoria: Quando/quem/o quê
```

### Talking Points:
- **Por que Lakehouse?** Tradicionais data lakes sofrem com data quality; warehouses são caros. Lakehouse é o melhor dos dois.
- **Delta Lake garante ACID**: Mesmo com 1M+ updates/dia, dados ficam consistentes.
- **Escalabilidade**: Spark processa petabytes em paralelo; ideal para big data.
- **Versionamento**: Rollback a qualquer ponto no tempo (time travel com Delta).

---

# SLIDE 4: Design de Machine Learning (0:25 - 0:35)

## Título: "Coração: Modelo de Predição de Preços"

### Problema de ML:

```
Tipo: REGRESSÃO
Entrada: Features do hóspede + reserva (8-10 features)
Saída: average_price (valor contínuo: $50-$500)
Métrica: RMSE, MAE, R²
```

### Dados de Treinamento:

```
Dataset: 40,000 reservas históricas (18 meses)
├─ Features Numéricas (7):
│  ├─ number_of_adults: 1-4
│  ├─ number_of_children: 0-2
│  ├─ number_of_weekend_nights: 0-5
│  ├─ number_of_week_nights: 0-7
│  ├─ car_parking_space: 0-1 (sim/não)
│  ├─ special_requests: 0-5
│  └─ lead_time: 0-500 (dias de antecedência)
│
└─ Features Categóricas (4):
   ├─ type_of_meal: Breakfast, Half Board, Full Board, etc.
   ├─ room_type: Standard, Deluxe, Suite, etc.
   ├─ arrival_month: Jan-Dec (sazonalidade)
   └─ market_segment_type: Aviation, Complementary, Corporate, etc.

Target: average_price (preço em $)
```

### Algoritmo: LightGBM

```
Por que LightGBM?
├─ ✅ Excelente para dados tabulares
├─ ✅ Rápido (10x mais rápido que XGBoost em 1M+ registros)
├─ ✅ Lida bem com features categóricas (sem encoding)
├─ ✅ Feature importance built-in (explainabilidade)
└─ ✅ Suporta GPU (training em segundos)

Hiperparâmetros (otimizados via Optuna):
├─ learning_rate: 0.05 (trade-off learning speed vs. overfitting)
├─ n_estimators: 200 (número de árvores)
└─ max_depth: 3 (profundidade, controla complexidade)
```

### Pipeline de Pré-processamento:

```
[Raw Data] → [Pipeline Sklearn]
             ├─ Categóricas: CatToIntTransformer (ordinal encoding)
             ├─ Numéricas: PassThrough (sem scaling, LGB é robusto)
             └─ Saída: Features prontos para LGB

Benefício: Pipeline garante transformações idênticas em treino/teste/produção
```

### Split de Dados (Temporal):

```
Baseline: Último 18 meses de dados

Split:
├─ Treino: 12 meses (histórico) → Treinar modelo
├─ Validação: 1 mês (sobreposição) → Tuning de hiperparâmetros
└─ Teste: 1 mês (futuro) → Avaliar performance real

❌ Evitado: Random split (causa data leakage - modelo "vê" futuro)
✅ Usado: Temporal split (respira realidade: treina passado, testa futuro)
```

### Métricas de Avaliação:

```
RMSE (Root Mean Squared Error):
├─ Sensível a outliers (grandes erros são penalizados)
├─ Unidade: $ (dólar)
└─ Target: <$15 (±5% do preço médio $300)

MAE (Mean Absolute Error):
├─ Robusto a outliers
├─ Unidade: $
└─ Threshold de alerta: >$30 (vai em alert.yml)

R² (Coeficiente de Determinação):
├─ Quanto da variância é explicada pelo modelo
├─ Range: 0-1 (melhor é 1)
└─ Target: >0.85
```

### Diagram de Fluxo:

```
[Training Data] → [Pré-processamento] → [LightGBM] → [Modelo Treinado]
                  (Features eng.)      (Fit)       (Binary + Info)
                       ↓                 ↓            ↓
                 [Categorical]    [Hyperparameters] [Signature]
                 [Numerical]      [Cross-validation] [Metrics]
                 
                                      ↓
                              [Avaliação em Test Set]
                              ├─ RMSE: 12.5$ ✓
                              ├─ MAE: 9.3$ ✓
                              └─ R²: 0.88 ✓
                              
                              ↓ (Passa? → Produção)
```

### Talking Points:
- **Por que Regressão?** Preço é contínuo, não discreta (não é "barato/caro", é valor exato).
- **LightGBM vs. Deep Learning?** Para tabulares, tree-based é melhor. Deep learning é overkill e mais lento.
- **Split Temporal é crítico**: Se misturássemos treino/teste aleatoriamente, modelo aprenderia padrões do futuro (ilusão).
- **Feature engineering é 80% do trabalho**: Boas features > bom modelo.

---

# SLIDE 5: MLOps e Pipeline de Produção (0:35 - 0:45)

## Título: "Infraestrutura: Automação e Confiabilidade"

### O que é MLOps?

```
Machine Learning Operations = DevOps + DataOps + MLDev

Objetivo: Automatizar ciclo de vida de ML
├─ Data → Code → Model → Serving → Monitoring → (Feedback Loop)
└─ Com foco em: Reprodutibilidade, Escalabilidade, Confiabilidade

Em Analogia: 
├─ Software: Write code → Test → Deploy → Monitor
└─ ML: Experiment → Track → Register → Serve → Monitor
```

### Pipeline MLOps (Databricks Asset Bundles):

```
Trigger: Job agendado (segunda-feira, 6h)
   ↓
[Task 1: Pré-processamento]
├─ Executa: scripts/preprocess_data.py
├─ Input: Dados brutos (data/booking.csv + dados de produção)
├─ Output: Tabela Silver (mlops_dev.hotel_booking.hotel_booking)
└─ Tempo: ~5 min
   ↓
[Task 2: Treinamento + Avaliação]
├─ Executa: scripts/train_register_model.py
├─ Input: Tabela Silver (train/test split temporal)
├─ Output: Modelo registrado em Unity Catalog com alias 'latest-model'
├─ Métricas: RMSE, MAE, R² loggadas em MLflow
└─ Tempo: ~10 min (inclui tuning)
   ↓
[Task 3: Validação e Deploy]
├─ Checklist:
│  ├─ Modelo novo melhor que anterior? (RMSE anterior < novo?)
│  ├─ Performance no teste aceitável? (R² > 0.85?)
│  └─ Sem regressão em subgrupos? (MAE por room_type ok?)
├─ Se passa: Promove alias 'latest-model' → novo modelo
├─ Se falha: Rollback, notifica, mantém modelo anterior
└─ Tempo: <1 min
   ↓
[Task 4: Serving Online]
├─ Endpoint REST atualizado com novo modelo
├─ Feature Store sincronizado
├─ API disponível em: https://databricks-workspace/api/models/hotel-booking/invocations
└─ Latência: <100ms por predição
   ↓
[Monitoramento Contínuo]
├─ Lakehouse Monitoring detecta drift:
│  ├─ Data drift: Distribuição de features muda? (KS test)
│  ├─ Label drift: Preços do mercado desviaram? (novo trend?)
│  └─ Feature drift: Entrada do hóspede mudou? (ex.: mais crianças pós-Covid)
├─ Alertas: Email se MAE > 30 ou drift p-value < 0.05
└─ Dashboard: Real-time performance + histórico
```

### MLflow: Rastreamento de Experimentos

```
Cada run captura:
├─ Código (git SHA, branch, commit message)
├─ Dados (tabelas usadas, versões Delta)
├─ Hiperparâmetros (learning_rate, n_estimators, max_depth)
├─ Métricas (RMSE, MAE, R², training time)
├─ Artefatos (modelo .pkl, gráficos, confusion matrix)
├─ Tags (ambiente, usuário, experimento ID)
└─ Timestamp

Benefício:
├─ Reprodutibilidade: Qualquer run pode ser recriada (mesmos dados/código)
├─ Auditoria: Saber exatamente qual modelo foi deployado quando
└─ Comparação: Escolher melhor entre múltiplos experimentos via UI
```

### Feature Store: Consistência Train ↔ Serve

```
Problema sem Feature Store:
Data Scientist treina modelo com features criadas manualmente
   ↓
Durante serving, features são recalculadas diferente (bug, versão old, etc.)
   ↓
Modelo faz predições ruins (treinou em Features A, servidor usa Features B)

Solução com Feature Store:
[Feature Table: hotel_booking_price_preds]
├─ Primary Key: Booking_ID
├─ Features: Predicted_BookingPrice, lead_time_normalized, etc.
└─ Armazenado em: mlops_dev.hotel_booking.hotel_booking_price_preds

Durante Treinamento:
Lookup features da tabela → Treina modelo
   ↓
Durante Serving:
API request com Booking_ID → Lookup features da mesma tabela → Predição

Garantia: Features idênticas em treino e produção
```

### Ambientes Isolados (Dev/Acc/Prd):

```
Dev (Desenvolvimento):
├─ Dados: Sintéticos ou subset dos reais
├─ Frequência de re-treino: Diária (experimenta rápido)
├─ Alertas: Mais lentos (pode tolerar falhas)
├─ Usuários: Data scientists, eng
└─ Objetivo: Inovação, testes rápidos

Acc (Acceptance/Staging):
├─ Dados: Réplica de produção (sem PII)
├─ Frequência: Semanal (como produção)
├─ Alertas: Iguais a produção
├─ Usuários: Product managers, stakeholders
└─ Objetivo: Validar antes de produção

Prd (Produção):
├─ Dados: 100% dos dados reais
├─ Frequência: Semanal (segunda 6h)
├─ Alertas: Críticos, 24/7
├─ Usuários: Aplicações, endpoints REST
└─ Objetivo: Predições em tempo real para negócio
```

### Rollback e Safety:

```
Se algo der errado em produção:
├─ Modelo novo tá ruim? → Reverte para versão anterior (1 clique)
├─ Dados corrompidos? → Rollback tabela Delta a ponto no tempo
├─ Serve degradado? → Scale up endpoint, ou use modelo anterior
└─ Tudo automatizado via Databricks asset bundles
```

### Diagram Completo:

```
[Dados Brutos] 
    ↓ (Job Agendado: Segunda 6h)
[Pré-processamento] 
    ↓ 
[Silver Layer] 
    ↓ 
[Treinamento MLflow] 
    ↓ 
[Validação + Promotion] 
    ↓ 
[Serving Endpoint] 
    ↓ 
[Aplicação/REST API]
    ↓
[Monitoramento Contínuo]
    ↓ (Se drift/performance ruim) 
[Alerta] → [Re-treina] (loop feedback)
```

### Talking Points:
- **CI/CD para ML**: Automação reduz erros manuais e acelera inovação.
- **Rastreabilidade é legal**: GDPR exige saber por que modelo fez decisão (auditoria).
- **Feature Store evita bug clássico**: Model serving vs. training mismatches (real problema em produção).
- **Rollback é crítico**: Produção sempre tem fallback seguro.

---

# SLIDE 6: Demo Prática / Walkthrough (0:45 - 0:55)

## Título: "Vendo na Prática"

### Parte 1: Estrutura do Código (2 min)

```
Mostrar no VS Code:

mlops-databricks/
├─ pyproject.toml          ← Dependências (MLflow, Databricks, LGB, Optuna)
├─ project_config.yml      ← Config: features, hiperparâmetros, ambientes
├─ databricks.yml          ← Deploy config: targets (dev/acc/prd)
│
├─ src/hotel_booking/      ← Código principal (Python package)
│  ├─ config.py            ← Carrega config.yml (validação Pydantic)
│  ├─ models/
│  │  ├─ lightgbm_model.py ← Classe LightGBMModel (treina/loga/registra)
│  │  ├─ pyfunc_model_wrapper.py ← PyFunc wrapper para MLflow
│  │  └─ serving.py        ← Cria endpoint REST
│  └─ data/
│     ├─ data_loader.py    ← Carrega dados com split temporal
│     └─ data_processor.py ← Limpeza e feature engineering
│
├─ scripts/                ← Scripts para jobs
│  ├─ preprocess_data.py   ← Task 1 (pre-processamento)
│  ├─ train_register_model.py ← Task 2 (treinamento)
│  └─ refresh_monitor.py   ← Task 4 (monitoramento)
│
├─ notebooks/              ← Notebooks para exploração (dev)
│  ├─ chapter2_preprocess_data.py
│  ├─ chapter3_1.experiment_tracking_demo.py
│  ├─ chapter4_1.model_serving.py
│  ├─ chapter4_2.feature_serving.py
│  └─ chapter4_3.model_serving_feature_lookup.py
│
└─ resources/              ← Configs de deploy
   ├─ ml_pipeline.yml      ← Define job com tasks 1-4
   ├─ ml_monitoring.yml    ← Configuração de monitoramento
   └─ alert.yml            ← Define alertas (MAE > 30)
```

### Parte 2: Rodando um Notebook (3 min)

**Cenário**: Abrir `notebooks/chapter3_1.experiment_tracking_demo.py` no Databricks

```python
# Imports
import mlflow
from hotel_booking.config import ProjectConfig
from hotel_booking.data.data_loader import DataLoader
from hotel_booking.models.lightgbm_model import LightGBMModel

# Setup
cfg = ProjectConfig.from_yaml("../project_config.yml", env="dev")
spark = SparkSession.builder.getOrCreate()

# Load data com split temporal
loader = DataLoader(spark, cfg)
X_train, y_train, X_test, y_test = loader.split(
    test_months=1, 
    train_months=12
)

# Treinar modelo
model = LightGBMModel(config=cfg)
model.train(X_train, y_train)

# Log em MLflow
with mlflow.start_run(experiment_name="/Shared/hotel-booking-training"):
    mlflow.log_params(cfg.parameters.model_dump())
    mlflow.log_metrics({
        "rmse": 12.5,
        "mae": 9.3,
        "r2": 0.88
    })
    mlflow.sklearn.log_model(model.pipeline, "model")
    mlflow.log_artifact("artifacts/plot_actual_vs_pred.png")

# Resultado: 
# ✓ Métricas aparece em MLflow UI
# ✓ Modelo salvo e pronto para registrar no catalog
# ✓ Histórico de experimentos acessível para comparação
```

**Mostrar no MLflow UI**:
- Experiment: `/Shared/hotel-booking-training`
- Run com métricas, parâmetros e artefatos
- Botão "Register Model" → Registra em Unity Catalog

### Parte 3: Visualizando Feature Store (2 min)

**Ir para Databricks UI → Machine Learning → Feature Store**

```
Feature Table: mlops_dev.hotel_booking.hotel_booking_price_preds
├─ Primary Key: Booking_ID
├─ Features:
│  ├─ Predicted_BookingPrice (float)
│  └─ ... [other features]
├─ Última atualização: 2 horas atrás
├─ Tamanho: 5.3 GB
└─ Change Data Feed: Habilitado (tracks histórico)

Feature Spec: return_hotel_booking_prices
├─ Lookup Key: Booking_ID
├─ Features: [Predicted_BookingPrice]
└─ Online Serving: Habilitado
```

**Demonstrar lookup**:
```python
from databricks.feature_engineering import FeatureEngineeringClient

fe = FeatureEngineeringClient()
features = fe.get_feature_lookup_table(
    spec_name="mlops_dev.hotel_booking.return_hotel_booking_prices",
    lookup_key={"Booking_ID": "BK123456"}
)
# Output: {"Predicted_BookingPrice": 287.50}
```

### Parte 4: Vendo o Dashboard de Monitoramento (2 min)

**Ir para Databricks UI → SQL → Explore → hotel-booking-monitor-dashboard**

```
Dashboard mostra:
├─ [Card 1] Predições do Dia: 2,847
├─ [Card 2] MAE Atual: 9.2$ (threshold: 30$, ✓ green)
├─ [Card 3] % de Predictions > $500: 2% (drift warning?)
├─ [Card 4] Latência P95: 78ms (target <100ms, ✓)
├─ [Card 5] Trending: MAE últimas 7 dias
│  └─ Gráfico: Dia 1: 8.5 → Dia 2: 9.1 → ... → Dia 7: 9.2
│     (✓ Estável, sem trend de degradação)
├─ [Card 6] Drift Detector: Features
│  └─ lead_time: KS=0.12 (✓ no drift, p>0.05)
│  └─ room_type: Chi2=1.8 (✓ ok)
└─ [Card 7] Alertas: 0 alertas ativos (histórico: 3 alerts semana passada)
```

**Explicar Alertas**:
- Alert: "MAE > 30" configurado em `resources/alert.yml`
- Query: `SELECT COUNT(*) * 100.0 / COUNT(*) WHERE mean_absolute_error > 30`
- Trigger: Email para maria@cauchy.io
- Frequência: Daily check

---

# SLIDE 7: Próximos Passos e Q&A (0:55 - 1:00)

## Título: "Para Você Começar Agora"

### Próximos Passos (se implementar):

#### Fase 1: Setup (Semana 1)
- [ ] Criar workspace Databricks
- [ ] Habilitar Unity Catalog
- [ ] Clonar repositório
- [ ] Instalar `databricks-cli` e autenticar

#### Fase 2: Configurar Dados (Semana 2)
- [ ] Carregar `data/booking.csv` em Delta (Bronze)
- [ ] Rodar `notebooks/chapter2_preprocess_data.py` (Silver layer)
- [ ] Validar qualidade com alertas

#### Fase 3: Treinar Modelo (Semana 3)
- [ ] Rodar `notebooks/chapter3_1.experiment_tracking_demo.py`
- [ ] Comparar experimentos em MLflow
- [ ] Registrar melhor modelo em Unity Catalog

#### Fase 4: Deploy (Semana 4)
- [ ] Configurar `databricks.yml` com seu workspace
- [ ] Executar `databricks bundle deploy --target dev`
- [ ] Rodar `notebooks/chapter4_1.model_serving.py` (criar endpoint)

#### Fase 5: Monitorar (Semana 5)
- [ ] Configurar alertas (resources/alert.yml)
- [ ] Agendar job `ml-pipeline` (segunda 6h)
- [ ] Criar dashboard de monitoramento

### Recursos Úteis:

```
📚 Documentação:
├─ https://docs.databricks.com/
├─ https://docs.databricks.com/dev-tools/bundles/
├─ https://mlflow.org/docs/
└─ https://docs.databricks.com/machine-learning/feature-store/

🔗 Repositório:
└─ https://github.com/[owner]/mlops-databricks (este projeto)

📖 Livro (Baseado em):
└─ "MLOps with Databricks" - O'Reilly (capítulos 2-6)

🎓 Cursos:
├─ Databricks Academy (gratuito)
├─ Coursera: Machine Learning Engineering
└─ LinkedIn Learning: MLOps courses
```

### Benefícios Realizados (Resumo):

```
✓ Automação: Pipeline re-treina automaticamente (0 intervenção manual)
✓ Confiabilidade: Modelo anterior sempre disponível para rollback
✓ Governança: Auditoria completa (quem, quando, por quê)
✓ Escalabilidade: De 40k para 4M+ registros sem mudar código
✓ Velocidade: Ideia → Produção em 1 semana (vs. 2-3 meses sem MLOps)
✓ ROI: 5-10% aumento de receita via precificação otimizada
```

### Perguntas & Respostas (5 min):

**Q1: Quanto custa Databricks?**
- A: Pay-per-compute (~$0.40/DBU/hora). Para 1 modelo:
  - Dev: ~$50/mês (notebooks esporádicos)
  - Prd: ~$200/mês (job semanal + serving)
  - (Escala com volume de dados/queries)

**Q2: E se não quisermos Databricks?**
- A: Alternativas open-source:
  - Data: DuckDB, Apache Iceberg (Delta open-source)
  - ML: MLflow, Kubeflow
  - Serve: FastAPI + Docker
  - Mas: Você mesmo gerencia infraestrutura (mais complexo)

**Q3: Como lidar com dados sensíveis (PII)?**
- A: Unity Catalog tem:
  - Data masking: Automaticamente esconde PII em queries
  - Row-level security: Diferentes usuários vêem diferentes dados
  - Auditoria: Log de quem acessou qual dado

**Q4: Posso usar outro algoritmo além de LightGBM?**
- A: Sim! XGBoost, RandomForest, Neural Networks.
  - Código é modular (LightGBMModel herda de padrão reutilizável)
  - Trocar é 30 min (só editar `lightgbm_model.py`)

**Q5: Quantos dados preciso para treinar?**
- A: Mínimo 1000 amostras (nosso caso tem 40k+, ideal para LGB)
  - Menos dados: Random Forest melhor
  - Muito pouco (<100): Regressão linear simples
  - Muito (>1B): Deep learning em GPU

---

## EXTRA: Diagramas para Slides

### Diagram 1: Fluxo End-to-End

```
┌─────────────────────────────────────────────────────────────┐
│                   MLOps Pipeline Hotel Booking              │
└─────────────────────────────────────────────────────────────┘

DATA LAYER                ML LAYER             SERVING LAYER    OPS
┌──────────┐            ┌──────────┐         ┌──────────┐      ┌──────┐
│  Bronze  │─────────→  │ Feature  │────────→│ Endpoint │─────→│Alert │
│  (Raw)   │            │ Store    │         │  REST    │      │Drift │
└──────────┘            └──────────┘         └──────────┘      └──────┘
                             ↓                    ↓
┌──────────┐            ┌──────────┐         ┌──────────┐      ┌──────┐
│  Silver  │────────→   │ MLflow   │────────→│ Model    │     │ SLA  │
│ (Clean)  │            │Tracking  │         │ Version  │     │ Logs │
└──────────┘            └──────────┘         └──────────┘      └──────┘

 Databricks               Databricks            Databricks      Lakehouse
  Lakehouse                 MLflow              Model Serving    Monitoring
```

### Diagram 2: Arquitetura Temporal

```
Semana N-1: Dados Históricos → Treina Modelo A
                                      ↓
Semana N:   Dados Novos + A → Avalia Model A
                ↓                     ↓
            Serving A            Monitora
            (Online)             (Drift? Performance?)
                ↓                     ↓
            Predições             Se OK: Keep A
            (in real)             Se Bad: Treina B
```

### Diagram 3: Comparação (Com vs. Sem MLOps)

```
┌─────────────────────────────────────────────────────────────┐
│ SEM MLOps (Manual)                                          │
├─────────────────────────────────────────────────────────────┤
│ [Notebook] → [CSV Export] → [Manual Deploy] → [Monitor?]  │
│    ↑            ↑              ↑                ↑           │
│  Horas        Days           Manual          Nope         │
│  Dev           Wait          Error-prone               │
│  Scattered    Versioning     Rollback = ???            │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ COM MLOps (Automated - Databricks)                         │
├─────────────────────────────────────────────────────────────┤
│ [Git] → [DAB Deploy] → [Auto Retrain] → [Monitor Alerts]  │
│   ↑          ↑             ↑               ↑               │
│ Versioned   1-click      Weekly          24/7            │
│ Audited     Repeatable   Feedback Loop   Drift+Perf      │
│ Reproducible Rollback    Automatic       Auto-action    │
└─────────────────────────────────────────────────────────────┘
```

---

## NOTAS PARA APRESENTADOR

- **Timing**: Cumprir 60 min rigorosamente (13-15 min para demo é crítico)
- **Público**: Ajustar detalhe técnico conforme plateia (CDO → foco negócio; Engineers → foco arquitetura)
- **Demo Falhar**: Ter screenshots como backup
- **Próxima Sessão**: Ofereça hands-on workshop (2-3h) para quem quer aprender mais
- **Slides Visuais**: Usar cores, não puro texto (sugestão: Databricks brand colors: azul + white)

---

## Última Slide: Obrigado!

```
"MLOps com Databricks: Do Experimento à Produção"

                        ✓ Automação
                        ✓ Confiabilidade
                        ✓ Escalabilidade
                        ✓ Governança

Comece Hoje: bit.ly/mlops-databricks-hotel

Dúvidas? Encontre-me no Slack/Email
```

---

**Fim da Apresentação**
