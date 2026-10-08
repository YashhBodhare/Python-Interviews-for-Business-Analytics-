def required_amount(row):
    try:
        return row["amount"]
    except KeyError as exc:
        raise ValueError("Missing required amount") from exc
assert required_amount({"amount": 0}) == 0
try:
    required_amount({})
except ValueError as exc:
    assert isinstance(exc.__cause__, KeyError)
else:
    raise AssertionError("Missing field accepted")
