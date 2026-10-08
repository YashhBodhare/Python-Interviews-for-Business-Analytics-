from copy import deepcopy
raw = [{"amount": 100, "tags": ["imported"]}]
clean = deepcopy(raw)
clean[0]["tags"].append("validated")
assert raw[0]["tags"] == ["imported"]
