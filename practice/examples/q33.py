class UnsupportedCurrencyError(Exception):
    pass
def validate_currency(value):
    if value not in {"INR", "USD"}:
        raise UnsupportedCurrencyError(value)
    return value
assert validate_currency("INR") == "INR"
try:
    validate_currency("XYZ")
except UnsupportedCurrencyError:
    pass
else:
    raise AssertionError("Unsupported currency accepted")
