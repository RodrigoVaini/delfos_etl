# 🚀 Delfos ETL Pipeline

Este projeto implementa um pipeline completo de ETL conforme especificação do documento técnico, envolvendo:

* Banco de dados **Fonte (PostgreSQL)**
* API **FastAPI** para exposição dos dados
* Banco de dados **Alvo (PostgreSQL)**
* Processo de **ETL em Python**
* Orquestração com **Dagster**
* Execução via **Docker e Docker Compose**

---

# 🧠 Arquitetura da Solução

```
[ PostgreSQL (Fonte) ]
          ↓
     FastAPI (API)
          ↓
      ETL (httpx + pandas)
          ↓
[ PostgreSQL (Alvo) ]
          ↓
      Dagster (orquestração)
```

---

# 📁 Estrutura do Projeto

```
.
├── api/              # API FastAPI (fonte de dados)
├── etl/              # Script de ETL
├── dagster/          # Orquestração Dagster
├── scripts/          # Scripts auxiliares (seed)
├── docker-compose.yml
├── .env
├── .gitignore
└── README.md
```

---

# ⚙️ Tecnologias Utilizadas

* Python 3.11
* FastAPI
* PostgreSQL
* SQLAlchemy
* Pandas
* HTTPX
* Dagster
* Docker / Docker Compose

---

# 🔐 Configuração de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```
SOURCE_DB_HOST=
SOURCE_DB_PORT=
SOURCE_DB_NAME=
SOURCE_DB_USER=
SOURCE_DB_PASSWORD=

TARGET_DB_HOST=
TARGET_DB_PORT=
TARGET_DB_NAME=
TARGET_DB_USER=
TARGET_DB_PASSWORD=

API_BASE_URL=
```

---

# ▶️ Como Executar o Projeto

## 1. Subir os containers

```
docker compose up -d --build
```

---

## 2. Iniciar e popular bancos de dados

```
python3 scripts/init_target_db.py
python3 scripts/seed_source_db.py
```

Gera dados com frequência de **1 minuto por 10 dias**, conforme solicitado no documento.

---

## 3. Acessar API

Swagger:

```
http://localhost:8000/docs
```

Exemplo de chamada:

```
GET /data?start=2025-01-01T00:00:00&end=2025-01-01T23:59:59&variables=wind_speed&variables=power
```

---

## 4. Executar ETL manualmente

```
python etl/app/etl.py 2025-01-01
```

---

## 5. Acessar Dagster

```
http://localhost:3000
```

* Selecionar o asset `etl_asset`
* Escolher uma data (partition)
* Executar

---

# 🔄 Pipeline ETL

## Extract

* Consome API via `httpx`
* Filtra por intervalo de data

## Transform

* Agregação 10-minutal:

  * média
  * mínimo
  * máximo
  * desvio padrão
* Normalização (wide → long)

## Load

* Inserção no banco alvo via SQLAlchemy
* Mapeamento automático de `signal_id`
* Uso de UPSERT para evitar duplicidade

---

# 📊 Modelagem do Banco Alvo

## Tabela `signal`

| id | name |
| -- | ---- |

## Tabela `data`

| timestamp | signal_id | value |
| --------- | --------- | ----- |

---

# 🧠 Decisões Técnicas

* Separação clara de responsabilidades (API / ETL / Orquestração)
* Uso de `.env` para configuração sensível
* Transformação desacoplada (`transform.py`)
* Uso de `ON CONFLICT DO NOTHING` para integridade
* Dagster com **partição diária**

---

# ⏰ Orquestração (Dagster)

* Asset particionado por dia
* Execução agendada:

```
0 2 * * *  (diariamente às 02:00)
```

---

# 🚀 Diferenciais

* Arquitetura modular e escalável
* Pipeline desacoplado
* Código preparado para produção
* Uso de boas práticas (Docker, env, ETL clean)
* Idempotência parcial (signals)

---

# 🔧 Melhorias Futuras

* Controle de duplicidade na tabela `data`
* ETL incremental
* Retry automático (API)
* Logging estruturado
* Monitoramento

---

# 👨‍💻 Autor

Rodrigo Vaini de Freitas

---

# 📌 Observações

* O projeto pode ser executado integralmente via Docker
* Não há dependências externas além dos containers
* Os dados são simulados conforme especificação do documento

---
