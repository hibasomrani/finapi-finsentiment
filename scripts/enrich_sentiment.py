"""Calcule le sentiment des news qui n'en ont pas encore."""

import logging
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import SessionLocal
from models import NewsItem
from sentiment import analyze_batch


def main(batch_size: int = 32) -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
    log = logging.getLogger(__name__)

    with SessionLocal() as session:
        rows = session.query(NewsItem).filter(NewsItem.sentiment_label.is_(None)).all()
        log.info("News a enrichir : %d", len(rows))
        if not rows:
            return 0

        for i in range(0, len(rows), batch_size):
            chunk = rows[i : i + batch_size]
            texts = [(r.title + " " + (r.summary or "")) for r in chunk]
            results = analyze_batch(texts)
            for r, res in zip(chunk, results, strict=True):
                r.sentiment_label = res.label
                r.sentiment_score = res.score
            session.commit()
            log.info("Batch %d-%d traite", i, i + len(chunk))

    return len(rows)


if __name__ == "__main__":
    n = main()
    print(f"Enrichies : {n}")
