from functools import wraps
def min_rows(required):
    def decorate(fn):
        @wraps(fn)
        def wrapper(rows):
            if len(rows) < required:
                raise ValueError("Insufficient rows")
            return fn(rows)
        return wrapper
    return decorate
@min_rows(2)
def total(rows):
    return sum(rows)
assert total([10, 20]) == 30
try:
    total([])
except ValueError:
    pass
else:
    raise AssertionError("Empty input accepted")
