class CountCalls:
    def __init__(self, fn):
        self.fn = fn
        self.calls = 0
    def __call__(self, *args, **kwargs):
        self.calls += 1
        return self.fn(*args, **kwargs)
@CountCalls
def total(values):
    return sum(values)
assert total([5]) == 5
assert total([10]) == 10 and total.calls == 2
