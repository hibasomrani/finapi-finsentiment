"""Point d'entree HF Spaces. Pre-remplit la DB si vide,
puis lance le dashboard Streamlit."""
import os
import sys
from pathlib import Path

# Add root and dashboard to path
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent / "dashboard"))

from db import SessionLocal, init_db
from models import PriceRecord


def bootstrap_data():
    """Si la DB est vide, lancer un mini ETL au demarrage."""
    init_db()
    with SessionLocal() as session:
        if session.query(PriceRecord).count() > 0:
            return
    print("DB vide, lancement bootstrap ETL...")
    from etl.prices_etl import ingest_prices
    from etl.news_etl import ingest_news
    from scripts.enrich_sentiment import main as enrich

    for t in ["AAPL", "MSFT", "GOOGL", "TSLA"]:
        ingest_prices(t, period="1mo")
        ingest_news(t)
    enrich()
    print("Bootstrap termine.")


if os.getenv("BOOTSTRAP", "1") == "1":
    bootstrap_data()

exec(open(Path(__file__).parent / "dashboard" / "app.py").read())