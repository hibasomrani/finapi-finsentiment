"""Dashboard interactif d'analyse de sentiment financier."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from datetime import datetime

import api_client as api
import streamlit as st
from charts import SENT_COLORS, price_line_chart, sentiment_pie_chart

# -------- Configuration de la page --------
st.set_page_config(
    page_title="FinSentiment Dashboard",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

# -------- Sidebar --------
with st.sidebar:
    st.title("Controles")
    st.caption("Configurez votre vue ci-dessous.")

    api_ok = api.get_health()
    if api_ok:
        st.success("API connectee")
    else:
        st.error("API injoignable")
        st.info("Lancez 'python app.py' dans un autre terminal.")
        st.stop()

    stats = api.get_db_stats()
    available_tickers = stats.get("tickers", [])
    if not available_tickers:
        st.warning("Base vide. Lancez 'python scripts/run_etl.py AAPL MSFT'.")
        st.stop()

    ticker = st.selectbox("Ticker", available_tickers)

    if st.button("Refresh maintenant"):
        st.cache_data.clear()
        st.rerun()

    st.divider()
    st.caption(
        f"DB: {stats['prices_count']} prix | {stats['news_count']} news "
        f"({stats['news_enriched']} avec sentiment)"
    )

# -------- En-tete --------
st.title(f":chart_with_upwards_trend: FinSentiment - {ticker}")
st.caption("Dashboard interactif - prix, news, sentiment FinBERT")


# -------- Donnees --------
@st.cache_data(ttl=60)
def load_prices(t: str):
    return api.get_db_prices(t)


@st.cache_data(ttl=60)
def load_news(t: str):
    return api.get_db_news(t)


@st.cache_data(ttl=60)
def load_summary(t: str):
    return api.get_sentiment_summary(t)


prices = load_prices(ticker)
news = load_news(ticker)
sentiment = load_summary(ticker)

# -------- Metriques en haut --------
col1, col2, col3, col4 = st.columns(4)
if prices:
    last = prices[0]
    prev = prices[1] if len(prices) > 1 else last
    delta = last["close"] - prev["close"]
    col1.metric("Dernier cours", f"{last['close']:.2f}", f"{delta:+.2f}")
    col2.metric("Date", last["date"])
    col3.metric("News stockees", len(news))
    total_sent = sum(sentiment.values()) or 1
    pos_share = sentiment.get("positive", 0) / total_sent * 100
    col4.metric("Sentiment positif", f"{pos_share:.0f}%")

st.divider()

# -------- Graphiques --------
g1, g2 = st.columns([2, 1])
with g1:
    st.subheader("Evolution du prix")
    st.plotly_chart(price_line_chart(prices), use_container_width=True)
with g2:
    st.subheader("Distribution sentiment")
    if sentiment:
        st.plotly_chart(sentiment_pie_chart(sentiment), use_container_width=True)
    else:
        st.info("Aucun sentiment calcule. Lancez 'enrich_sentiment.py'.")

# -------- Liste de news colorees --------
st.subheader(f"Dernieres news - {ticker}")
if not news:
    st.info("Aucune news en base.")
else:
    for n in news[:15]:
        sent = n.get("sentiment_label") or "neutral"
        color = SENT_COLORS.get(sent, "#94A3B8")
        st.markdown(
            f"<div style='border-left: 4px solid {color};"
            f" padding: 8px 14px; margin: 4px 0;"
            f" background: #F8FAFC;'>"
            f"<b>{n['title']}</b><br>"
            f"<small style='color:#64748B'>{n['publisher']} - "
            f"{n['published_at'][:16]} - "
            f"<span style='color:{color}; font-weight:bold;'>{sent.upper()}</span>"
            f"</small></div>",
            unsafe_allow_html=True,
        )

st.divider()
st.caption(f"Mis a jour : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
