import os
from dotenv import load_dotenv
from graph import build_graph
from state import AgentState
from datetime import datetime

load_dotenv()


def run_agent(ticker: str, sector: str = None) -> str:
    """
    Point d'entrée principal.
    Retourne le brief d'analyse en Markdown.
    """
    graph = build_graph()

    initial_state: AgentState = {
        "ticker": ticker.upper(),
        "sector": sector,
        "price_data": None,
        "fundamentals": None,
        "historical_data": None,
        "news_articles": None,
        "sentiment_score": None,
        "sentiment_reasoning": None,
        "sentiment_full": None,
        "key_insights": None,
        "report": None,
        "errors": [],
    }

    print(f"\n🚀 Lancement de l'analyse pour : {ticker.upper()}\n{'='*50}")

    final_state = graph.invoke(initial_state)

    if final_state.get("errors"):
        print(f"\n⚠️  Erreurs non bloquantes :")
        for e in final_state["errors"]:
            print(f"   - {e}")

    print(f"\n{'='*50}\n✅ Analyse terminée\n")
    return final_state["report"]


if __name__ == "__main__":
    import sys

    ticker = sys.argv[1] if len(sys.argv) > 1 else "AAPL"
    sector = sys.argv[2] if len(sys.argv) > 2 else None

    report = run_agent(ticker, sector)
    print(report)

    os.makedirs("reports", exist_ok=True)
    output_file = f"reports/{ticker}_{datetime.now().strftime('%Y%m%d_%H%M')}.md"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"📄 Rapport sauvegardé : {output_file}")