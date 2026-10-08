from functools import wraps
def passthrough(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        return fn(*args, **kwargs)
    return wrapper
@passthrough
def paid_revenue(values):
    """Sum eligible paid values."""
    return sum(values)
assert paid_revenue.__name__ == "paid_revenue"
assert paid_revenue.__wrapped__([5, 10]) == 15
