# nodes/report.py
import os
import sys
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from state import AgentState


def format_number(value, prefix="", suffix="", billions=False):
    """Formate les grands nombres pour la lisibilité."""
    if value is None:
        return "N/A"
    if billions:
        return f"{prefix}{value / 1_000_000_000:.2f}B{suffix}"
    return f"{prefix}{value}{suffix}"


def sentiment_emoji(sentiment):
    return {"bullish": "🟢", "neutral": "🟡", "bearish": "🔴"}.get(sentiment, "⚪")


def report_node(state: AgentState) -> AgentState:
    """
    Nœud 4 : Génère le brief d'analyse final en Markdown.
    Assemble toutes les données du state en un rapport structuré.
    """
    ticker = state["ticker"]
    errors = state.get("errors") or []

    print(f"📝 [report_node] Génération du rapport pour {ticker}...")

    try:
        fundamentals = state.get("fundamentals") or {}
        price_data = state.get("price_data") or {}
        news_articles = state.get("news_articles") or []
        sentiment = state.get("sentiment_score", "N/A")
        reasoning = state.get("sentiment_reasoning", "")
        key_insights = state.get("key_insights") or []
        sentiment_full = state.get("sentiment_full") or {}
        risks = sentiment_full.get("risks") or []
        opportunities = sentiment_full.get("opportunities") or []

        date_str = datetime.now().strftime("%d/%m/%Y %H:%M")
        emoji = sentiment_emoji(sentiment)

        # Variation jour
        day_change = price_data.get('day_change_pct')
        day_arrow = "▲" if day_change and day_change > 0 else "▼"
        day_color = "+" if day_change and day_change > 0 else ""

        report = f"""# 📊 Analyse financière — {fundamentals.get('company_name', ticker)} ({ticker})
> Généré le {date_str} | Secteur : {fundamentals.get('sector', 'N/A')} | {fundamentals.get('industry', 'N/A')}

---

## {emoji} Sentiment global : {sentiment.upper() if sentiment else 'N/A'}
**Confiance** : {sentiment_full.get('confidence', 'N/A')}

{reasoning}

---

## 💰 Prix & Performance
| Métrique | Valeur |
|---|---|
| Prix actuel | {format_number(price_data.get('current_price'), prefix=price_data.get('currency', '') + ' ')} |
| Variation du jour | {day_arrow} {day_color}{day_change}% |
| Performance 1 an | {format_number(price_data.get('1y_return_pct'), suffix='%')} |
| Volatilité annualisée | {format_number(price_data.get('1y_volatility'), suffix='%')} |
| Plus haut 52 semaines | {format_number(price_data.get('52w_high'))} |
| Plus bas 52 semaines | {format_number(price_data.get('52w_low'))} |

---

## 📈 Fondamentaux
| Métrique | Valeur |
|---|---|
| Market Cap | {format_number(fundamentals.get('market_cap'), billions=True)} |
| PE Ratio (trailing) | {round(fundamentals.get('pe_ratio'), 2) if fundamentals.get('pe_ratio') else 'N/A'} |
| PE Ratio (forward) | {round(fundamentals.get('forward_pe'), 2) if fundamentals.get('forward_pe') else 'N/A'} |
| EPS | {round(fundamentals.get('eps'), 2) if fundamentals.get('eps') else 'N/A'} |
| Marge nette | {round(fundamentals.get('profit_margin') * 100, 2) if fundamentals.get('profit_margin') else 'N/A'}% |
| ROE | {round(fundamentals.get('roe') * 100, 2) if fundamentals.get('roe') else 'N/A'}% |
| Dette / Capitaux propres | {format_number(fundamentals.get('debt_to_equity'))} |
| Free Cash Flow | {format_number(fundamentals.get('free_cashflow'), billions=True)} |
| Recommandation analystes | {fundamentals.get('recommendation', 'N/A').upper()} |
| Prix cible moyen | {round(fundamentals.get('analyst_target'), 2) if fundamentals.get('analyst_target') else 'N/A'} |

---

## 💡 Points clés
{chr(10).join(f"- {insight}" for insight in key_insights) if key_insights else "- N/A"}

---

## 🚀 Opportunités
{chr(10).join(f"- {opp}" for opp in opportunities) if opportunities else "- N/A"}

## ⚠️ Risques
{chr(10).join(f"- {risk}" for risk in risks) if risks else "- N/A"}

---

## 📰 Actualités récentes
{chr(10).join(f"- [{a['title']}]({a['url']})" for a in news_articles) if news_articles else "- Aucune actualité trouvée"}

---
*Analyse générée automatiquement — ne constitue pas un conseil en investissement.*
"""

        print(f"✅ [report_node] Rapport généré ({len(report)} caractères)")

        return {
            **state,
            "report": report,
            "errors": errors,
        }

    except Exception as e:
        error_msg = f"[report_node] Erreur : {str(e)}"
        print(f"❌ {error_msg}")
        errors.append(error_msg)
        return {**state, "errors": errors}