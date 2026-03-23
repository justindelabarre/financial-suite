# core/data/fmp_client.py
# TODO (étape 2) : client Financial Modeling Prep
import os
import requests

FMP_BASE = "https://financialmodelingprep.com/api/v3"


def get_ratios(ticker: str) -> dict:
    """Retourne les ratios financiers depuis FMP."""
    raise NotImplementedError("À implémenter à l'étape 2")
