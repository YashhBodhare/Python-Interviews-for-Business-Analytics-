source = [10, -3, 20]
approved = [v for v in source if v >= 0]
assert sum(approved) == 30
assert list(approved) == [10, 20]
