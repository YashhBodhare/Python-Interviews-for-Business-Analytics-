from functools import wraps
runs = []
def tracked(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        runs.append(fn.__name__)
        return fn(*args, **kwargs)
    return wrapper
@tracked
def total(values):
    return sum(values)
assert total([20, 30]) == 50 and runs == ["total"]
