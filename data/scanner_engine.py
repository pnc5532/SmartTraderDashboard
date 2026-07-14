"""
Common Scanner Engine
Version 3.0

Shared functions used by:
- Swing Scanner
- Momentum Scanner
- Volume Scanner
- Volume Momentum Scanner
"""

from concurrent.futures import ThreadPoolExecutor


def parallel_scan(symbols, scan_function, max_workers=8):
    """
    Run scan_function(symbol) in parallel.
    """

    if not symbols:
        return []

    workers = min(max_workers, len(symbols))

    with ThreadPoolExecutor(max_workers=workers) as executor:
        results = list(executor.map(scan_function, symbols))

    return [r for r in results if r is not None]


def sort_results(rows, sort_by, ascending=False):
    """
    Generic sorting helper.
    """

    return sorted(
        rows,
        key=lambda x: x.get(sort_by, 0),
        reverse=not ascending
    )


def top_results(rows, limit=20):
    """
    Return top N rows.
    """

    return rows[:limit]


def calculate_price_strength(price_change):
    """
    Score based on price movement.
    """

    if price_change >= 5:
        return 40
    elif price_change >= 3:
        return 30
    elif price_change >= 1:
        return 15
    elif price_change <= -5:
        return 40
    elif price_change <= -3:
        return 30
    elif price_change <= -1:
        return 15

    return 0


def calculate_volume_strength(volume):
    """
    Score based on volume.
    """

    score = 0

    if volume["pass_avg20"]:
        score += 20

    if volume["pass_high15"]:
        score += 10

    if volume["ratio"] >= 3:
        score += 10
    elif volume["ratio"] >= 2.5:
        score += 5

    return score


def calculate_breakout_strength(breakout):
    """
    Score based on breakout.
    """

    score = 0

    if breakout["bull_breakout"]:
        score += 30

    if breakout["bear_breakdown"]:
        score += 30

    return score