import yfinance as yf
from state import AgentState


def financial_node(state: AgentState) -> AgentState:
    """
    Nœud 1 : Récupère les données financières via yfinance.
    - Prix actuel + variation jour
    - Fondamentaux (PE, market cap, EPS, dividende...)
    - Historique 1 an (pour comparaison historique)
    """
    ticker = state["ticker"]
    errors = state.get("errors") or []

    print(f"📊 [financial_node] Récupération données pour {ticker}...")

    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        # --- Prix actuel + variation jour ---
        current_price = info.get("currentPrice") or info.get("regularMarketPrice")
        previous_close = info.get("previousClose") or info.get("regularMarketPreviousClose")

        if current_price and previous_close:
            day_change = current_price - previous_close
            day_change_pct = (day_change / previous_close) * 100
        else:
            day_change = None
            day_change_pct = None

        price_data = {
            "current_price": current_price,
            "previous_close": previous_close,
            "day_change": round(day_change, 2) if day_change else None,
            "day_change_pct": round(day_change_pct, 2) if day_change_pct else None,
            "volume": info.get("volume"),
            "avg_volume": info.get("averageVolume"),
            "52w_high": info.get("fiftyTwoWeekHigh"),
            "52w_low": info.get("fiftyTwoWeekLow"),
            "currency": info.get("currency", "USD"),
        }

        # --- Fondamentaux ---
        fundamentals = {
            "company_name": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "eps": info.get("trailingEps"),
            "dividend_yield": info.get("dividendYield"),
            "beta": info.get("beta"),
            "pb_ratio": info.get("priceToBook"),
            "revenue": info.get("totalRevenue"),
            "profit_margin": info.get("profitMargins"),
            "debt_to_equity": info.get("debtToEquity"),
            "roe": info.get("returnOnEquity"),
            "free_cashflow": info.get("freeCashflow"),
            "analyst_target": info.get("targetMeanPrice"),
            "recommendation": info.get("recommendationKey"),
        }

        # --- Historique 1 an ---
        hist = stock.history(period="1y")

        if not hist.empty:
            historical_data = [
                {
                    "date": str(row.Index.date()),
                    "close": round(row.Close, 2),
                    "volume": int(row.Volume),
                }
                for row in hist.itertuples()
            ]

            # Stats historiques utiles pour le brief
            price_data["1y_return_pct"] = round(
                ((hist["Close"].iloc[-1] - hist["Close"].iloc[0]) / hist["Close"].iloc[0]) * 100, 2
            )
            price_data["1y_volatility"] = round(
                hist["Close"].pct_change().std() * (252 ** 0.5) * 100, 2  # volatilité annualisée
            )
        else:
            historical_data = []
            errors.append(f"[financial_node] Pas d'historique disponible pour {ticker}")

        print(f"✅ [financial_node] OK — {fundamentals.get('company_name')} | "
              f"Prix: {price_data.get('current_price')} {price_data.get('currency')} | "
              f"PE: {fundamentals.get('pe_ratio')}")

        return {
            **state,
            "price_data": price_data,
            "fundamentals": fundamentals,
            "historical_data": historical_data,
            "errors": errors,
        }

    except Exception as e:
        error_msg = f"[financial_node] Erreur pour {ticker} : {str(e)}"
        print(f"❌ {error_msg}")
        errors.append(error_msg)
        return {**state, "errors": errors}
