a = ("CRM", "C001")
b = tuple(["CRM", "C001"])
assert a == b and hash(a) == hash(b)
assert len({a, b}) == 1
