events = []
try:
    amount = int("100")
except ValueError:
    events.append("invalid")
else:
    events.append("success")
finally:
    events.append("cleanup")
assert amount == 100 and events == ["success", "cleanup"]
