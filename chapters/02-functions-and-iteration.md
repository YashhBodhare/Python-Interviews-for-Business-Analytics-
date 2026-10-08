# 🟡 Functions, decorators and iteration
[← Study hub](../README.md) · [Cheat sheet](../CHEAT_SHEET.md) · [Practice](../practice/README.md)

> [!TIP]
> Attempt the question aloud before expanding the answer. Each business case is hypothetical; describe it as “I would” unless it reflects work you actually did.

<a id="py-11"></a>
## PY-11 · Decorators for shared behaviour

**Interview question**

What happens when a function is decorated?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

A decorator receives the function and returns the object that will replace its name. A common decorator returns a wrapper that adds logging or checks around the original call. Keep business calculations in the original function and preserve its metadata with functools.wraps.

### Small worked example

```python
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
```

The assertions show the expected result. [Run this example](../practice/examples/q11.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A team needs consistent run tracking across several KPI calculations.

**Why I use this:** Use a shared wrapper for operational tracking without changing each KPI formula.

**What I validate:** Confirm decorated and undecorated calculations produce the same metric.

**Business value:** Improve traceability without introducing divergent business logic.

**Interview-ready response**

> “I would use a shared wrapper for operational tracking without changing each KPI formula. I would confirm decorated and undecorated calculations produce the same metric. This would help the business improve traceability without introducing divergent business logic.”

</details>

---

<a id="py-12"></a>
## PY-12 · Decorator ordering

**Interview question**

How does stacking two decorators change execution order?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

For @outer above @inner, Python constructs outer(inner(function)). At call time the outer wrapper starts first; its code after the inner call runs on the way back out. Order matters for validation, authorisation, caching and logging.

### Small worked example

```python
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
```

The assertions show the expected result. [Run this example](../practice/examples/q12.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A report should validate input before it records a successful computation.

**Why I use this:** Agree the wrapper order and distinguish start, completion and failure events.

**What I validate:** Inspect an event trace for both valid and failing inputs.

**Business value:** Avoid misleading audit logs.

**Interview-ready response**

> “I would agree the wrapper order and distinguish start, completion and failure events. I would inspect an event trace for both valid and failing inputs. This would help the business avoid misleading audit logs.”

</details>

---

<a id="py-13"></a>
## PY-13 · Preserving function metadata

**Interview question**

Why use functools.wraps in a wrapper?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

`wraps` copies selected metadata such as the name and documentation, and sets __wrapped__ to the original callable. This improves inspection and debugging. The wrapper still executes; metadata preservation does not make its behaviour identical to the original.

### Small worked example

```python
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
```

The assertions show the expected result. [Run this example](../practice/examples/q13.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** Support needs to identify which KPI function failed in an automated reporting run.

**Why I use this:** Preserve meaningful names and documentation in shared wrappers.

**What I validate:** Inspect the decorated name and original callable link.

**Business value:** Make incidents easier to diagnose.

**Interview-ready response**

> “I would preserve meaningful names and documentation in shared wrappers. I would inspect the decorated name and original callable link. This would help the business make incidents easier to diagnose.”

</details>

---

<a id="py-14"></a>
## PY-14 · Configurable decorators

**Interview question**

How do you pass a setting into a decorator?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

Use a factory that accepts the setting and returns a decorator. That decorator receives the function and returns its wrapper. This separates configuration from the operation being wrapped. Do not hide important business settings from users of the function.

### Small worked example

```python
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
```

The assertions show the expected result. [Run this example](../practice/examples/q14.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** Different report types have different minimum row-count requirements.

**Why I use this:** Configure the minimum explicitly and return a clear validation error if it is not met.

**What I validate:** Check the exact threshold and an empty dataset.

**Business value:** Stop incomplete extracts from being presented as complete reports.

**Interview-ready response**

> “I would configure the minimum explicitly and return a clear validation error if it is not met. I would check the exact threshold and an empty dataset. This would help the business stop incomplete extracts from being presented as complete reports.”

</details>

---

<a id="py-15"></a>
## PY-15 · Stateful callable wrappers

**Interview question**

When might a callable class be useful as a decorator?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

A class implementing __call__ can wrap a function while retaining explicit state, such as a run counter. A closure can also hold state; a class is useful when inspection or additional methods make the design clearer. Shared state still needs appropriate concurrency protection.

### Small worked example

```python
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
```

The assertions show the expected result. [Run this example](../practice/examples/q15.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** An analyst wants a count of how many times a report calculation is invoked during a run.

**Why I use this:** Use a small stateful wrapper and define when counters reset.

**What I validate:** Verify counts across repeated calls and separate reporting runs.

**Business value:** Detect unexpected repeated work.

**Interview-ready response**

> “I would use a small stateful wrapper and define when counters reset. I would verify counts across repeated calls and separate reporting runs. This would help the business detect unexpected repeated work.”

</details>

---

<a id="py-16"></a>
## PY-16 · Iterator and generator protocols

**Interview question**

How does a generator relate to an iterator?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

An iterator returns successive values through next() and signals completion with StopIteration. A generator function contains yield; calling it creates a generator object, which is an iterator. Its body progresses as the consumer requests values.

### Small worked example

```python
def rejected(rows):
    for row in rows:
        if row["amount"] < 0:
            yield row["id"]
g = rejected([{"id": 1, "amount": 20}, {"id": 2, "amount": -5}])
assert iter(g) is g and next(g) == 2
assert list(g) == []
```

The assertions show the expected result. [Run this example](../practice/examples/q16.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A validation workflow should emit rejected orders without collecting every rejection first.

**Why I use this:** Yield exceptions as they are found and let the consumer decide how to store them.

**What I validate:** Check filtering and the end-of-stream condition.

**Business value:** Support incremental exception handling.

**Interview-ready response**

> “I would yield exceptions as they are found and let the consumer decide how to store them. I would check filtering and the end-of-stream condition. This would help the business support incremental exception handling.”

</details>

---

<a id="py-17"></a>
## PY-17 · Materialising results for reuse

**Interview question**

What is the trade-off between a reusable list and a single-pass generator?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

A list keeps results for reuse; a generator avoids materialising all outputs at once but cannot be rewound. A generator is not a guarantee of constant total memory: it may retain a large source or build large intermediate values. Measure the complete pipeline.

### Small worked example

```python
source = [10, -3, 20]
approved = [v for v in source if v >= 0]
assert sum(approved) == 30
assert list(approved) == [10, 20]
```

The assertions show the expected result. [Run this example](../practice/examples/q17.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** The same set of approved amounts is needed for both a total and a customer-facing detail report.

**Why I use this:** Materialise the approved result if it fits memory, or design a repeatable source reader.

**What I validate:** Verify both consumers receive the same eligible population.

**Business value:** Keep summary and detail reports consistent.

**Interview-ready response**

> “I would materialise the approved result if it fits memory, or design a repeatable source reader. I would verify both consumers receive the same eligible population. This would help the business keep summary and detail reports consistent.”

</details>

---

<a id="py-18"></a>
## PY-18 · Delegating with yield from

**Interview question**

What does yield from add to a generator?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

`yield from` yields values from another iterable. With a subgenerator it also delegates parts of the generator protocol and receives the subgenerator's return value. For a simple sequence it is a readable alternative to a loop that yields each element.

### Small worked example

```python
def rows_from_batches(batches):
    for batch in batches:
        yield from batch
assert list(rows_from_batches([[101, 102], [], [103]])) == [101, 102, 103]
```

The assertions show the expected result. [Run this example](../practice/examples/q18.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** Monthly sales batches should feed one continuous validation stream.

**Why I use this:** Delegate iteration over each batch while preserving its agreed order.

**What I validate:** Check empty batches and ensure every row appears once.

**Business value:** Process batches uniformly without manual concatenation.

**Interview-ready response**

> “I would delegate iteration over each batch while preserving its agreed order. I would check empty batches and ensure every row appears once. This would help the business process batches uniformly without manual concatenation.”

</details>

---

<a id="py-19"></a>
## PY-19 · Consumed iterators

**Interview question**

Why can a second pass through a generator return no records?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

An iterator remembers its current position. After it reaches the end, it stays exhausted. Create a new iterator from a repeatable source or materialise results when another pass is needed. zip(strict=True) detects length mismatches; it does not rewind inputs or prevent consumption during detection.

### Small worked example

```python
g = (x for x in [100, 200])
assert list(g) == [100, 200]
assert list(g) == []
reusable = [100, 200]
assert sum(reusable) == sum(reusable) == 300
```

The assertions show the expected result. [Run this example](../practice/examples/q19.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A preview consumes records before the revenue calculation runs.

**Why I use this:** Use a reusable list for the small preview dataset or reopen a repeatable source.

**What I validate:** Run preview and total in the same workflow and check the total is not silently zero.

**Business value:** Prevent misleading reports caused by accidental consumption.

**Interview-ready response**

> “I would use a reusable list for the small preview dataset or reopen a repeatable source. I would run preview and total in the same workflow and check the total is not silently zero. This would help the business prevent misleading reports caused by accidental consumption.”

</details>

---

<a id="py-20"></a>
## PY-20 · Memoisation with cache and lru_cache

**Interview question**

When is caching useful, and how do the two decorators differ?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

`cache` retains results without a size bound; `lru_cache(maxsize=N)` limits entries and evicts less recently used ones. Inputs must be hashable. Use caching when repeated inputs should produce a reusable result, and define invalidation when underlying business data can change. Neither decorator guarantees one execution for simultaneous first calls.

### Small worked example

```python
from functools import lru_cache
@lru_cache(maxsize=16)
def classification(product_id, rules_version):
    return "core" if product_id == "P01" else "other"
assert classification("P01", "v1") == "core"
classification("P01", "v1")
assert classification.cache_info().hits == 1
```

The assertions show the expected result. [Run this example](../practice/examples/q20.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** Many reports repeatedly look up the same stable product classification.

**Why I use this:** Cache a versioned classification lookup and define a refresh policy.

**What I validate:** Check repeated calls, changed versions and memory limits.

**Business value:** Reduce repeated work without serving stale classifications.

**Interview-ready response**

> “I would cache a versioned classification lookup and define a refresh policy. I would check repeated calls, changed versions and memory limits. This would help the business reduce repeated work without serving stale classifications.”

</details>

---
