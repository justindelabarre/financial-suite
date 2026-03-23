from typing import TypedDict, Optional, List, Dict, Any


class AgentState(TypedDict):
    """
    State partagé entre tous les nœuds du graph.
    Chaque nœud lit ce dont il a besoin et enrichit le state.
    """

    # --- Input utilisateur ---
    ticker: str                          # ex: "AAPL"
    sector: Optional[str]                # ex: "tech" (optionnel)

    # --- Données financières (yfinance) ---
    price_data: Optional[Dict[str, Any]]         # prix actuel, variation, volume
    fundamentals: Optional[Dict[str, Any]]       # PE, PB, EPS, market cap...
    historical_data: Optional[List[Dict]]        # historique 1 an de prix

    # --- News (Tavily) ---
    news_articles: Optional[List[Dict[str, str]]]  # liste de {title, url, content, date}

    # --- Analyse LLM ---
    sentiment_score: Optional[str]       # "bullish" / "neutral" / "bearish"
    sentiment_reasoning: Optional[str]   # explication du sentiment
    key_insights: Optional[List[str]]    # points clés identifiés par le LLM
    sentiment_full: Optional[Dict[str, Any]]   # analyse complète du LLM

    # --- Output final ---
    report: Optional[str]                # brief final en Markdown

    # --- Meta ---
    errors: Optional[List[str]]          # log des erreurs non bloquantes
