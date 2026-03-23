# core/indicators/fundamentals.py
# TODO : calculs de ratios dérivés (PEG, EV/EBITDA...)

def peg_ratio(pe: float, growth_rate: float) -> float:
    if not growth_rate:
        return None
    return pe / growth_rate
