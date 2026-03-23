# test_nodes.py
from dotenv import load_dotenv
load_dotenv()

from nodes.financial import financial_node
from nodes.news import news_node
from nodes.sentiment import sentiment_node
from nodes.report import report_node

state = {
    "ticker": "AAPL", "sector": None, "price_data": None,
    "fundamentals": None, "historical_data": None,
    "news_articles": None, "sentiment_score": None,
    "sentiment_reasoning": None, "key_insights": None,
    "sentiment_full": None, "report": None, "errors": [],
}

state = financial_node(state)
state = news_node(state)
state = sentiment_node(state)
state = report_node(state)

print(state["report"])