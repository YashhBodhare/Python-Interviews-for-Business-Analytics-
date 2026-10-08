def label_sales(value):
    if value is None:
        return "unknown"
    return "zero" if value == 0 else "recorded"
assert label_sales(None) == "unknown"
assert label_sales(0) == "zero"
