def renewal_label(days: int | None) -> str:
    return "unknown" if days is None else f"{days} days"
assert renewal_label(None) == "unknown"
assert renewal_label(0) == "0 days"
