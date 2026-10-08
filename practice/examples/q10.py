orders = [{"gross": 100, "refund": 20}, {"gross": 60, "refund": 10}]
net_values = [net for o in orders if (net := o["gross"] - o["refund"]) > 50]
assert net_values == [80]
