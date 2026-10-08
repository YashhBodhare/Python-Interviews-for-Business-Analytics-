g = (x for x in [100, 200])
assert list(g) == [100, 200]
assert list(g) == []
reusable = [100, 200]
assert sum(reusable) == sum(reusable) == 300
