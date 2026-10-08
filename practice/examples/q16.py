def rejected(rows):
    for row in rows:
        if row["amount"] < 0:
            yield row["id"]
g = rejected([{"id": 1, "amount": 20}, {"id": 2, "amount": -5}])
assert iter(g) is g and next(g) == 2
assert list(g) == []
