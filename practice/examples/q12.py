events = []
def mark(name):
    def decorate(fn):
        def wrapper():
            events.append(name + " before")
            result = fn()
            events.append(name + " after")
            return result
        return wrapper
    return decorate
@mark("outer")
@mark("inner")
def report():
    return 100
assert report() == 100
assert events == ["outer before", "inner before", "inner after", "outer after"]
