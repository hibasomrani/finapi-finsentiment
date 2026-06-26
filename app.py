def bootstrap_data():
    """Si la DB est vide, lancer un mini ETL au demarrage."""
    init_db()
    with SessionLocal() as session:
        if session.query(PriceRecord).count() > 0:
            return
    print("DB vide, lancement bootstrap ETL...")
    try:
        from etl.prices_etl import ingest_prices
        from etl.news_etl import ingest_news
        from scripts.enrich_sentiment import main as enrich

        for t in ["AAPL", "MSFT", "GOOGL", "TSLA"]:
            try:
                ingest_prices(t, period="1mo")
                ingest_news(t)
            except Exception as e:
                print(f"Warning: could not fetch {t}: {e}")
        enrich()
    except Exception as e:
        print(f"Bootstrap failed: {e}")
    print("Bootstrap termine.")