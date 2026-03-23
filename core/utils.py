# core/utils.py

def format_number(value, prefix="", suffix="", billions=False):
    """Formate les grands nombres pour la lisibilité."""
    if value is None:
        return "N/A"
    if billions:
        return f"{prefix}{value / 1_000_000_000:.2f}B{suffix}"
    return f"{prefix}{value}{suffix}"
