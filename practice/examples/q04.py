orders = [{"status": "paid", "amount": 120}, {"status": "pending", "amount": 50}]
revenue = sum(o["amount"] for o in orders if o["status"] == "paid")
assert revenue == 120
