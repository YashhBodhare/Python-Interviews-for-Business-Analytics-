# 🟩 Python cheat sheet for Business Analytics

[← Study hub](README.md) · [Interview chapters](README.md#-your-combined-library) · [Practice](practice/README.md)

> [!TIP]
> Before coding, define the input schema, record grain, missing-value policy, business calculation and expected output. A compact function is valuable only when it implements the right rule.

## 🧰 Twelve everyday tools

| Tool | Simple reminder | Business application | Important check |
|---|---|---|---|
| `zip(a, b, strict=True)` | Pair corresponding values; strict detects unequal lengths, Python 3.10+ | Pair labels with validated observations | Position is not a join key; strict does not rewind consumed inputs |
| `enumerate(rows, start=1)` | Index and value together | Give exception rows a readable position | A displayed position is not a stable record ID |
| `any()` / `all()` | Short-circuit truth testing | Detect any failed rule or require all rules to pass | `any([])` is False; `all([])` is True; check required data exists |
| `sorted(..., key=...)` | Return a stable sorted list | Rank overdue invoices | Define ties and missing values; input is not changed |
| `map()` / `filter()` | Lazy iterators in Python 3 | Transform or select records | A comprehension may be clearer; performance depends on the workload |
| `itertools` | Compose iteration | Flatten batches, group ordered data, calculate running totals | `groupby` groups consecutive keys, not all equal keys anywhere |
| `functools` | Reuse or adapt callables | Configure helpers or cache stable reference lookups | Cache size, hashable inputs and refresh policy |
| `collections` | Purpose-built containers | Count exceptions, bucket orders, maintain a queue | Choose the structure from required operations |
| `dict.get` / `setdefault` | Read with fallback / insert a default if missing | Optional attributes or grouped rows | Do not replace required-field validation with a silent fallback |
| `pathlib.Path` | Work with filesystem paths | Read a local approved configuration | Use explicit encoding and an authorised path |
| `dataclass` | Generate common record methods | Represent report metadata | Fresh defaults; frozen is not deep immutability |
| `typing.Protocol` | Describe a structural interface | Swap source adapters | Type hints do not validate runtime business data |

### Pairing, numbering and rule checks

```python
customers = ["C01", "C02"]
scores = [70, 85]
paired = dict(zip(customers, scores, strict=True))
numbered = list(enumerate(customers, start=1))
assert paired == {"C01": 70, "C02": 85}
assert numbered == [(1, "C01"), (2, "C02")]
rules = [True, True]
ready = bool(rules) and all(rules)
assert ready and not any([False, False])
```

Only zip observations if their order and one-to-one correspondence are already established. For independently sourced customer data, join by a validated key instead.

### Sorting, mapping and filtering

```python
rows = [{"id": 2, "amount": 100}, {"id": 1, "amount": 100}, {"id": 3, "amount": 50}]
ranked = sorted(rows, key=lambda row: (-row["amount"], row["id"]))
amounts = list(map(lambda row: row["amount"], rows))
eligible = [row for row in rows if row["amount"] >= 100]
assert [row["id"] for row in ranked] == [1, 2, 3]
assert amounts == [100, 100, 50] and len(eligible) == 2
```

Use a named `def` for a complex, documented business rule.

### Iterator toolkit

```python
from itertools import chain, groupby, accumulate
rows = [{"city": "Thane", "amount": 20}, {"city": "Mumbai", "amount": 10}, {"city": "Thane", "amount": 30}]
ordered = sorted(rows, key=lambda row: row["city"])
by_city = {
    city: sum(row["amount"] for row in group)
    for city, group in groupby(ordered, key=lambda row: row["city"])
}
assert by_city == {"Mumbai": 10, "Thane": 50}
assert list(chain([10, 20], [30])) == [10, 20, 30]
assert list(accumulate([10, 20, 30])) == [10, 30, 60]
```

For time-based running totals, first establish chronology and a tie-breaker. Convert each group to a list if it needs to survive advancement of the shared groupby iterator.

### Function adaptation and caching

```python
from functools import partial, reduce, lru_cache
from operator import add
assert reduce(add, [10, 20, 30], 0) == 60

def net(gross, refund=0):
    return gross - refund
with_standard_refund = partial(net, refund=10)
assert with_standard_refund(100) == 90

@lru_cache(maxsize=16)
def product_tier(product_id, rules_version):
    return "core" if product_id == "P01" else "other"
assert product_tier("P01", "v1") == "core"
```

`cache` is unbounded memoisation, available in Python 3.9+. Do not cache volatile prices without a deliberate invalidation strategy. Caching is not a guaranteed once-only mechanism for concurrent calls.

### Collections and dictionary defaults

```python
from collections import Counter, defaultdict, deque
statuses = ["paid", "failed", "paid"]
assert Counter(statuses)["paid"] == 2
buckets = defaultdict(list)
buckets["Thane"].append("O01")
queue = deque(["O01", "O02"])
assert queue.popleft() == "O01"
row = {"id": "O01"}
assert row.get("note", "not supplied") == "not supplied"
row.setdefault("issues", []).append("missing date")
assert row["issues"] == ["missing date"]
```

`setdefault` changes the dictionary when its key is missing. Its default expression is evaluated at the call, even if insertion is not required.

### Paths, dataclasses and protocols

```python
from pathlib import Path
from dataclasses import dataclass, field
from typing import Protocol

config_path = Path("config") / "report.json"
# Actual file read, when the approved file exists:
# text = config_path.read_text(encoding="utf-8")

@dataclass
class Run:
    run_id: str
    issues: list[str] = field(default_factory=list)

class Reader(Protocol):
    def read(self) -> list[dict]: ...

first, second = Run("A"), Run("B")
first.issues.append("missing source")
assert second.issues == []
```

## 🕳️ Eight traps to explain clearly

| Trap | Correct approach | Business risk avoided |
|---|---|---|
| Mutable default argument | Default to None; create a new container inside | Exceptions leaking between client runs |
| Late-bound closure | Bind the intended value, or use an explicit factory | Every generated rule using the last threshold |
| `is` vs `==` | Value comparison with ==; sentinel checks with is | Wrong ID or amount comparisons |
| Integer/string interning | Treat reuse as an implementation detail | Environment-dependent comparison bugs |
| Float arithmetic | Use `math.isclose` for approximate values; Decimal from strings for exact decimal rules | Unexpected equality or financial rounding |
| `[[]] * n` aliasing | `[[] for _ in range(n)]` for independent lists | One customer's update changing every bucket |
| Iterator exhaustion | Rebuild from a repeatable source or materialise intentionally | Empty second-pass calculations |
| Mutable class attribute | Put per-instance mutable state in __init__ or a default factory | State leaking between independent records |

```python
from decimal import Decimal, ROUND_HALF_UP
from math import isclose
assert isclose(0.1 + 0.2, 0.3)
amount = Decimal("2.675").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
assert amount == Decimal("2.68")
independent = [[] for _ in range(3)]
independent[0].append("O01")
assert independent[1] == []
```

Python's built-in round uses ties-to-even for exact halfway cases, for example `round(0.5) == 0`; binary representation can affect apparent decimal ties. Agree precision and rounding with Finance; Decimal does not choose the business policy for you. `is True` is appropriate only when exactly the boolean singleton is required; it is not a substitute for all truth testing. Numeric objects outside CPython's small-integer cache can still be reused, so “257 is always a different object” is incorrect.

## ⏱️ Data-structure decision table

Typical CPython complexity reminders; dictionary/set costs are averages with suitable hashing. Constants and input distributions still matter.

| Operation | List / tuple | Dictionary / set | deque | heapq on list |
|---|---|---|---|---|
| Index access | O(1) | Dict key lookup O(1) average; set has no positional indexing | O(1) near ends, O(n) in middle | Minimum at index 0: O(1) |
| Membership | O(n) | O(1) average, O(n) pathological worst case | O(n) | O(n) |
| Append right | List O(1) amortised; tuple immutable | Insert O(1) average | O(1) via append | O(log n) via heappush |
| Remove from left | List pop(0): O(n); tuple immutable | Not a queue operation | O(1) via popleft | heappop minimum: O(log n) |
| Find value | O(n) | Dict values search O(n); key lookup differs | O(n) | O(n) |
| Minimum / maximum | O(n) | O(n) over chosen keys/values | O(n) | Minimum O(1); maximum O(n) |
| Full sorting | O(n log n) worst-case comparison sorting into a list | Sort keys/items into a list | Convert and sort | Heap order is not fully sorted order |

Choose **set** for membership, **dict** for key-based lookups, **deque** for a FIFO queue and **heapq** for a priority queue. Dictionary insertion order is a language guarantee from Python 3.7; it is not sorted-key order. Counter.most_common depends on the number of distinct keys and the requested limit, not a universal fixed cost.

## 🐼 pandas: from data to business measures

Examples below use a fictional INR order dataset. Run the [business lab](practice/README.md) for checked results.

### Grouping and named aggregation

```python
import pandas as pd
df = pd.DataFrame([
    {"id": 1, "city": "Thane", "amount": 100, "status": "paid"},
    {"id": 2, "city": "Thane", "amount": 50, "status": "pending"},
    {"id": 3, "city": "Mumbai", "amount": 200, "status": "paid"},
])
paid = df.loc[df["status"].eq("paid")]
summary = paid.groupby("city", as_index=False).agg(
    revenue=("amount", "sum"), average=("amount", "mean"), orders=("id", "size")
)
assert summary["revenue"].sum() == 300
```

`size` counts rows; `count` excludes missing values in the selected column. groupby drops missing keys by default; use `dropna=False` when the approved population includes those groups. Consider `sum(min_count=1)` when an all-missing group must remain unknown rather than become zero.

### Merging without inflated totals

```python
customers = pd.DataFrame({"customer_id": [1, 2], "tier": ["Gold", "Silver"]})
orders = pd.DataFrame({"order_id": [101, 102, 103], "customer_id": [1, 1, 2], "amount": [100, 50, 200]})
enriched = orders.merge(customers, on="customer_id", how="left", validate="m:1", indicator=True)
assert len(enriched) == len(orders)
assert enriched["amount"].sum() == 350
```

| validate option | What it checks |
|---|---|
| `1:1` | Keys unique on both sides |
| `1:m` | Keys unique on the left |
| `m:1` | Keys unique on the right |
| `m:m` | Allows many-to-many; does not enforce uniqueness |

pandas can match missing join keys to each other, unlike ordinary SQL equality joins. Define a missing-key policy and validate reference uniqueness before merging. `indicator=True` helps expose unmatched records.

### Pivot and pivot_table

| Tool | Appropriate input | Duplicate row/column combinations |
|---|---|---|
| `pivot` | One value per combination | Raises an error |
| `pivot_table` | An aggregation is required | Aggregates using the specified rule; default is mean |

```python
wide = df.pivot_table(index="city", columns="status", values="amount", aggfunc="sum", fill_value=0)
assert wide.loc["Thane", "paid"] == 100
```

Use zero filling only when a missing combination truly means no activity. Do not silently replace an unknown measurement with zero.

### Vectorised calculations and group transforms

```python
lines = pd.DataFrame({"price": [100, 50], "qty": [2, 3]})
lines["total"] = lines["price"] * lines["qty"]
assert lines["total"].sum() == 350

df["city_rank"] = df.groupby("city")["amount"].rank(method="dense", ascending=False)
```

Prefer suitable built-in vectorised operations, agg or transform over row-wise apply. This is a design preference to benchmark, not a guaranteed 10× or 100× speedup. Some operations and data representations do not become faster simply because they look vectorised.

### Missing values, nullable types and explicit updates

```python
s = pd.Series([1, 2, None], dtype="Int64")
assert s.isna().tolist() == [False, False, True]
df.loc[df["amount"].gt(100), "review"] = "check"
```

Use isna/notna for missing-value tests. `pd.NA` and `np.nan` do not behave like ordinary equal values; pd.NA cannot be coerced to a boolean without ambiguity. `convert_dtypes()` can help select nullable types, but inspect the resulting schema rather than assuming every conversion fits the business rule.

Copy-on-Write is the default and only mode in pandas 3.0; it was optional in pandas 2.x. Use a single `.loc[mask, column] = value` assignment on the intended DataFrame. Chained assignment does not update the original under Copy-on-Write.

## ✅ Before reporting a result

- Agree the population, grain, units, currency and time window.
- Check missing values, duplicate IDs and join cardinality.
- Reconcile counts and totals before and after transformations.
- Keep source freshness and excluded rows visible.
- Test a small fixture by hand before scaling up.
- Explain the business meaning and limits of the result.
