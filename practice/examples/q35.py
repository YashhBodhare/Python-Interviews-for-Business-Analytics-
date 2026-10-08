handled = []
try:
    raise ExceptionGroup("validation", [ValueError("bad amount"), TypeError("bad type")])
except* ValueError as group:
    handled.append(("value", len(group.exceptions)))
except* TypeError as group:
    handled.append(("type", len(group.exceptions)))
assert handled == [("value", 1), ("type", 1)]
