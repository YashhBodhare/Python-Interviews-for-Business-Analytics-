invoices = [{"id": 2, "days": 10}, {"id": 1, "days": 10}, {"id": 3, "days": 20}]
queue = sorted(invoices, key=lambda r: (-r["days"], r["id"]))
assert [r["id"] for r in queue] == [3, 1, 2]
fns = [lambda threshold=t: threshold for t in (10, 20)]
assert [f() for f in fns] == [10, 20]
