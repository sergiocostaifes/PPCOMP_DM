# PPCOMP_DM
Dissertação de Mestrado - Sérgio Henrique Cerqueira Costa

# Otimização de PRD com Machine Learning
## Estudo de Caso – Banestes (PPCOMP/IFES)

Autor: Sérgio Henrique Cerqueira Costa  
Programa: Mestrado em Computação Aplicada – IFES  
Linha: Inteligência Artificial aplicada à Continuidade de Negócios  

---

## 🎯 Objetivo do Projeto

Desenvolver e validar um protótipo baseado em Machine Learning para:

1. Classificação automática de estados de execução do PRD (BEFORE / DURING / AFTER)
2. Priorização de manobras corretivas utilizando Learning to Rank (LambdaMART)

A arquitetura segue abordagem Design Science Research (DSR).

---

# 🧭 Pipeline Metodológico

O projeto é estruturado em notebooks modulares, cada um produzindo artefatos versionáveis e datasets intermediários em formato Parquet.

---

## 🔹 00_env_paths.ipynb
Configuração de ambiente:
- Montagem do Google Drive
- Definição de caminhos
- Seed global
- Verificação de versões

---

## 🔹 01_ingest_validate.ipynb
Ingestão e validação do dataset bruto:
Entrada:
- `01-raw/borg_traces_data.csv`

Saída:
- `02-processed/trace_raw_validated.parquet` (opcional)

Inclui:
- Checagem de schema
- Tipos
- Estatísticas básicas
- Verificação de consistência

---

## 🔹 02_clean_normalize.ipynb
Limpeza e normalização:
Entrada:
- CSV bruto ou parquet validado

Saída:
- `02-processed/google_trace_clean.parquet`

Inclui:
- Remoção da Hora 0
- Conversão de tipos
- Criação de colunas auxiliares
- Remoção de duplicatas

---

## 🔹 03_windowing_episodes.ipynb
Janelamento temporal e detecção de episódios:
Entrada:
- `google_trace_clean.parquet`

Saídas:
- `03-features/window_5min_base.parquet`
- `03-features/episodes_detected.parquet`

Inclui:
- Agregações por janela
- Identificação de eventos críticos

---

## 🔹 04_feature_engineering.ipynb
Engenharia de atributos:
Entrada:
- `window_5min_base.parquet`

Saída:
- `03-features/window_5min_features.parquet`

Inclui:
- Métricas de carga
- Taxas de falha
- Entropia/dispersão
- Atrasos e indicadores robustos

---

## 🔹 05_labeling_states.ipynb
Rotulagem supervisionada:
Entrada:
- Features
- Episódios detectados

Saída:
- `04-labeled/window_5min_labeled.parquet`

Rótulos:
- BEFORE
- DURING
- AFTER

---

## 🔹 06_baseline_rf.ipynb
Classificação com Random Forest:
Entrada:
- Dataset rotulado

Saídas:
- `models/rf_baseline.joblib`
- `reports/rf_metrics.json`

Métricas:
- Acurácia
- Precisão
- Revocação
- F1-score
- Matriz de confusão

---

## 🔹 07_error_analysis_iterate.ipynb
Análise de erros e refinamento.

---

## 🔹 08_ltr_dataset_build.ipynb
Construção do dataset para ranking:
Saída:
- `05-ltr/ltr_train.parquet`
- `05-ltr/ltr_valid.parquet`

---

## 🔹 09_lambdamart.ipynb
Treinamento do modelo de Learning to Rank:
Saída:
- Modelo LambdaMART
- Métricas NDCG e MAP

---

# 📂 Estrutura de Diretórios

mestrado-prd-ml/
│
├── notebooks/
├── src/
├── config/
├── reports/
├── models/
├── README.md
└── .gitignore


---

# 💾 Estratégia de Dados

- Dados brutos armazenados no Google Drive.
- Datasets intermediários em formato Parquet com compressão Snappy.
- Git versiona apenas código e metadados.
- Dados NÃO são versionados no repositório.

---

# 🧪 Reprodutibilidade

- Seed global fixa
- Pipeline incremental
- Notebooks modulares
- Validação cruzada estratificada

---

# 🚀 Ambiente de Execução

Principal:
- Google Colab

Alternativa:
- Execução local via ambiente Python 3.10+

---

# 🔐 Observações

Dados reais do Banestes são anonimizados e não fazem parte deste repositório público.
