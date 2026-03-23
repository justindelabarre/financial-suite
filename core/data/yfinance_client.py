# core/data/yfinance_client.py
# TODO (étape 2) : extraire la logique yfinance depuis agent/nodes/financial.py
import yfinance as yf


def get_price_data(ticker: str) -> dict:
    """Retourne le prix actuel + variation + 52w."""
    raise NotImplementedError("À implémenter à l'étape 2")


def get_fundamentals(ticker: str) -> dict:
    """Retourne les ratios fondamentaux."""
    raise NotImplementedError("À implémenter à l'étape 2")


def get_historical(ticker: str, period: str = "1y") -> list:
    """Retourne l'historique de prix."""
    raise NotImplementedError("À implémenter à l'étape 2")
