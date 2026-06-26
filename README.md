---
title: FinSentiment
emoji: 📈
colorFrom: blue
colorTo: yellow
sdk: streamlit
sdk_version: "1.58.0"
app_file: app.py
pinned: false
license: mit
---
![CI](https://github.com/hibasomrani/finapi-finsentiment/actions/workflows/ci.yml/badge.svg)
# finapi — API Flask pour cours boursiers

API REST Python/Flask qui expose des cours boursiers et news via yfinance + SQLite.

## Installation

```bash
cd C:\Users\somra\projets\finapi
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Lancement du serveur

```bash
python app.py
```

Le serveur démarre sur http://127.0.0.1:5000

## ETL — Ingestion des données

```bash
python scripts\run_etl.py AAPL MSFT GOOGL
```

## Endpoints Lab 1

### GET /health
```bash
curl http://localhost:5000/health
```

### GET /price/<ticker>
```bash
curl http://localhost:5000/price/AAPL
```

### GET /history/<ticker>?days=N
```bash
curl http://localhost:5000/history/MSFT?days=5
```

## Endpoints Lab 2

### GET /db/prices/<ticker>
Lit les prix stockés depuis SQLite.
```bash
curl http://localhost:5000/db/prices/AAPL
```

### GET /db/news/<ticker>
Lit les news stockées depuis SQLite.
```bash
curl http://localhost:5000/db/news/AAPL
```

## Gestion des erreurs

| Code | Cas |
|------|-----|
| 200  | Succès |
| 400  | Paramètre invalide |
| 404  | Ticker introuvable |
| 500  | Erreur interne |

## Auteur
Somra — 

## Dashboard

Lancer l'API Flask dans un terminal :
```bash
python app.py
```

Lancer le dashboard dans un second terminal :
```bash
streamlit run dashboard\app.py
```

Le dashboard s'ouvre sur http://localhost:8501