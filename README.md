# PPCOMP_DM
Dissertação de Mestrado – Sérgio Henrique Cerqueira Costa  
Programa de Pós-Graduação em Computação Aplicada (PPCOMP) – IFES  

---

# Otimização de Planos de Recuperação de Desastres (PRD) com Machine Learning

## Objetivo

Desenvolver e validar um protótipo baseado em Machine Learning para:

- Detecção e classificação automática de estados operacionais em ambientes distribuídos
- Identificação de episódios críticos (eventos anômalos)
- Classificação supervisionada de estados BEFORE / DURING / AFTER

A pesquisa segue abordagem **Design Science Research (DSR)**.

---

# Dataset Utilizado

Este repositório utiliza exclusivamente o dataset público:

**Google Cluster Trace (Borg Traces)**

Objetivo do uso:

- Simular ambiente distribuído de grande escala
- Modelar falhas e carga
- Construir séries temporais agregadas
- Detectar episódios críticos

Este repositório NÃO contém:
- Dados reais externos ao dataset público
- Logs institucionais
- Informações sensíveis
- Infraestrutura real

O dataset é utilizado como proxy experimental para validação metodológica da arquitetura proposta.

---

# Pipeline Metodológico

O projeto é estruturado em notebooks modulares e encadeados.
A granularidade temporal oficial adotada é de 5 minutos.          

## 00_env_paths.ipynb
Bootstrap do ambiente:
- Montagem automática do Google Drive
- Clone / atualização automática do repositório
- Definição de caminhos padrão
- Configuração de seed global

## 01_ingest_validate.ipynb
Objetivo: ingestão e validação inicial.
- Leitura do dataset bruto
- Validação de schema
- Tratamento de sentinelas temporais
- Estatísticas exploratórias iniciais

Saída:
- `trace_raw_validated.parquet`

---

## 02_clean_normalize.ipynb
Objetivo: limpeza e normalização temporal.
- Conversão de time para numérico
- Remoção de valores inválidos
- Criação de t_rel_us
- Remoção de artefatos temporais
- Persistência em formato Parquet

Saída:
- `google_trace_clean.parquet`

---

## 03_window_5min_base.ipynb
Objetivo: construção da base temporal agregada.
- Criação de minute_bucket (5 min = 300s)
- Agregações por janela:
  - events_total
  - failures_total
  - fail_rate
  - métricas opcionais (machines, jobs)
- Construção de série contínua (reindex)

Saídas:
- `window_5min_base.parquet`
- `window_5min_series.parquet`

Este notebook estabelece a granularidade oficial do modelo.

---

## 04_window_5min_episodes.ipynb
Objetivo: detecção automática de episódios críticos.
- Aplicação de limiar estatístico (μ + 2σ)
- Identificação de intervalos contínuos
- Consolidação de episódios

Cálculo de métricas por episódio:
- duração
- intensidade máxima
- média
- total de falhas

Saída:
- `episodes_detected.parquet`

Este notebook define a base objetiva para rotulagem supervisionada.

---

## 05_feature_engineering.ipynb
Objetivo: construção de atributos derivados para ML.
Inclui:
- Rolling mean (k janelas)
- Rolling std
- Indicadores de tendência
- Indicadores de aceleração de falhas
- Métricas robustas (p95, p99)
- Entropia / dispersão (se aplicável)

Saída:
- `window_5min_features.parquet`

---

## 06_labeling_states.ipynb
Objetivo: definição do ground truth supervisionado.
- Uso da tabela de episódios
- Rotulagem temporal:
  - BEFORE
  - DURING
  - AFTER
- Validação de consistência

Saída:
- `window_5min_labeled.parquet`

Este notebook formaliza o problema de classificação.

---

## 07_baseline_rf.ipynb
Objetivo: baseline supervisionado.
- Split temporal (train/test)
- Treinamento Random Forest
- Avaliação:
  - Accuracy
  - Precision
  - Recall
  - F1-score
  - Matriz de confusão
- Salvamento do modelo

Saídas:
- `rf_baseline.joblib`
- `rf_metrics.json`

---


# Estrutura do Repositório
PPCOMP_DM/
│
├── notebooks/
├── src/
├── config/
├── reports/
├── models/
├── README.md
└── .gitignore


---

# Estratégia de Dados

- Dados brutos armazenados no Google Drive
- Intermediários em formato Parquet (Snappy)
- Git versiona apenas código
- Datasets NÃO são versionados

---

# Reprodutibilidade

- Bootstrap automático do repositório
- Controle de versão via Git
- Pipeline incremental
- Seed fixa
- Ambiente principal: Google Colab

---

# Observação Importante

Este repositório é público e contém exclusivamente:

- Código acadêmico
- Dataset público
- Resultados experimentais
  
Não representa arquitetura real de nenhuma instituição financeira.
