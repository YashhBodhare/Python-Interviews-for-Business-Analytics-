rows = [{"id": 1, "tier": "Gold", "city": "Thane"}, {"id": 2, "tier": "Silver", "city": "Thane"}]
assert len({r["id"] for r in rows}) == len(rows)
tiers = {r["id"]: r["tier"] for r in rows}
cities = {r["city"] for r in rows}
assert tiers[2] == "Silver" and cities == {"Thane"}
