# nodes/sentiment.py
import os
import sys
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from groq import Groq
from state import AgentState


def sentiment_node(state: AgentState) -> AgentState:
    """
    Nœud 3 : Analyse le sentiment via LLM (Groq / llama3-70b).
    - Lit les news et les fondamentaux du state
    - Produit un sentiment bullish / neutral / bearish
    - Extrait les points clés
    """
    ticker = state["ticker"]
    errors = state.get("errors") or []

    print(f"🧠 [sentiment_node] Analyse sentiment pour {ticker}...")

    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        # --- Préparation du contexte pour le LLM ---
        fundamentals = state.get("fundamentals") or {}
        price_data = state.get("price_data") or {}
        news_articles = state.get("news_articles") or []

        # Résumé des news pour ne pas surcharger le prompt
        news_summary = "\n".join([
            f"- {a['title']} ({a['source']})"
            for a in news_articles
        ])

        prompt = f"""Tu es un analyste financier expert. Analyse les données suivantes pour {ticker} et fournis une analyse structurée.

## Données financières
- Prix actuel : {price_data.get('current_price')} {price_data.get('currency')}
- Variation du jour : {price_data.get('day_change_pct')}%
- Performance 1 an : {price_data.get('1y_return_pct')}%
- Volatilité annualisée : {price_data.get('1y_volatility')}%
- PE Ratio : {fundamentals.get('pe_ratio')}
- Forward PE : {fundamentals.get('forward_pe')}
- Market Cap : {fundamentals.get('market_cap')}
- Marge nette : {round(fundamentals.get('profit_margin') * 100, 2) if fundamentals.get('profit_margin') else 'N/A'}%
- ROE : {round(fundamentals.get('roe') * 100, 2) if fundamentals.get('roe') else 'N/A'}%
- Recommandation analystes : {fundamentals.get('recommendation')}
- Prix cible moyen : {fundamentals.get('analyst_target')}

## Actualités récentes
{news_summary}

## Ta mission
Réponds UNIQUEMENT en JSON valide avec cette structure exacte :
{{
    "sentiment": "bullish" | "neutral" | "bearish",
    "confidence": "high" | "medium" | "low",
    "reasoning": "explication concise en 2-3 phrases",
    "key_insights": ["insight 1", "insight 2", "insight 3"],
    "risks": ["risque 1", "risque 2"],
    "opportunities": ["opportunité 1", "opportunité 2"]
}}"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,   # faible température = réponses plus factuelles
            max_tokens=800,
        )

        raw = response.choices[0].message.content.strip()

        # Nettoyage si le LLM ajoute des backticks markdown
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]

        analysis = json.loads(raw)

        print(f"✅ [sentiment_node] OK — Sentiment: {analysis.get('sentiment').upper()} "
              f"({analysis.get('confidence')} confidence)")
        print(f"   💬 {analysis.get('reasoning')[:100]}...")

        return {
            **state,
            "sentiment_score": analysis.get("sentiment"),
            "sentiment_reasoning": analysis.get("reasoning"),
            "key_insights": analysis.get("key_insights", []),
            "errors": errors,
            # On stocke l'analyse complète pour le report_node
            "sentiment_full": analysis,
        }

    except json.JSONDecodeError as e:
        error_msg = f"[sentiment_node] Erreur parsing JSON : {str(e)}"
        print(f"❌ {error_msg}")
        errors.append(error_msg)
        return {**state, "errors": errors}

    except Exception as e:
        error_msg = f"[sentiment_node] Erreur : {str(e)}"
        print(f"❌ {error_msg}")
        errors.append(error_msg)
        return {**state, "errors": errors}