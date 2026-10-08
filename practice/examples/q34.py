class ImportValidationError(Exception):
    pass
def parse_amount(value):
    try:
        return int(value)
    except ValueError as exc:
        raise ImportValidationError("Amount must be an integer") from exc
try:
    parse_amount("unknown")
except ImportValidationError as exc:
    assert isinstance(exc.__cause__, ValueError)
else:
    raise AssertionError("Invalid amount accepted")
