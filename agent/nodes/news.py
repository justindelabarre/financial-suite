# nodes/news.py
import os
from tavily import TavilyClient
from state import AgentState
from datetime import datetime
current_year = datetime.now().year


import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def news_node(state: AgentState) -> AgentState:
    """
    Nœud 2 : Récupère les news récentes via Tavily.
    - Recherche par ticker + nom de la société
    - Retourne les 5 articles les plus récents
    """
    ticker = state["ticker"]
    errors = state.get("errors") or []

    # On enrichit la recherche avec le nom de la société si disponible
    company_name = (state.get("fundamentals") or {}).get("company_name", "")
    query = f"{company_name} {ticker} latest news {current_year}" if company_name else f"{ticker} latest news {current_year}"


    print(f"📰 [news_node] Recherche news pour {ticker} : '{query}'")

    try:
        client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

        response = client.search(
            query=query,
            search_depth="basic",    # "basic" = gratuit, "advanced" = plus de résultats
            max_results=5,
            include_answer=False,
            include_raw_content=False,
        )

        articles = []
        for result in response.get("results", []):
            articles.append({
                "title": result.get("title", ""),
                "url": result.get("url", ""),
                "content": result.get("content", ""),   # extrait de l'article
                "published_date": result.get("published_date", ""),
                "source": result.get("url", "").split("/")[2] if result.get("url") else "",
            })

        print(f"✅ [news_node] OK — {len(articles)} articles trouvés pour {ticker}")
        for a in articles:
            print(f"   • {a['title'][:80]}...")

        return {
            **state,
            "news_articles": articles,
            "errors": errors,
        }

    except Exception as e:
        error_msg = f"[news_node] Erreur pour {ticker} : {str(e)}"
        print(f"❌ {error_msg}")
        errors.append(error_msg)
        return {**state, "errors": errors}