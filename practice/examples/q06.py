def revenue(amounts, /, *, refund_amount=0):
    return sum(amounts) - refund_amount
assert revenue([100, 200], refund_amount=20) == 280
