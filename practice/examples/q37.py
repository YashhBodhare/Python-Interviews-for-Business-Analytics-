def normalise_id(value: int | str) -> str:
    return str(value).strip()
assert normalise_id(12) == "12"
assert normalise_id("0012") == "0012"
