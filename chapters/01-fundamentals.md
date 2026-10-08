# 🟢 Python foundations
[← Study hub](../README.md) · [Cheat sheet](../CHEAT_SHEET.md) · [Practice](../practice/README.md)

> [!TIP]
> Attempt the question aloud before expanding the answer. Each business case is hypothetical; describe it as “I would” unless it reflects work you actually did.

<a id="py-01"></a>
## PY-01 · Values, identity and missing inputs

**Interview question**

When would you compare with ==, and when would you use is?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

`==` compares values according to the type's equality rules. `is` checks whether two references point to the same object. Use `is None` for a missing-value sentinel and `==` for amounts, IDs and text. Identity checks also have legitimate uses with custom sentinel objects; they are not restricted to None or booleans.

### Small worked example

```python
discount = 0
assert discount is not None
left = [100, 200]
right = [100, 200]
assert left == right and left is not right
```

The assertions show the expected result. [Run this example](../practice/examples/q01.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A sales import contains a zero discount for some orders and no discount value for others.

**Why I use this:** Check for None explicitly so a valid zero is not treated as missing.

**What I validate:** Test None, zero and two separately created but equal values.

**Business value:** Keep missing-data exceptions separate from legitimate zero discounts.

**Interview-ready response**

> “I would check for None explicitly so a valid zero is not treated as missing. I would test None, zero and two separately created but equal values. This would help the business keep missing-data exceptions separate from legitimate zero discounts.”

</details>

---

<a id="py-02"></a>
## PY-02 · Mutable data and shared references

**Interview question**

How does mutability affect a data-cleaning workflow?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

Lists, dictionaries and sets can change in place. Integers, strings and tuples cannot change their own contents or structure. A tuple can still contain a mutable list. If two variables reference one mutable object, changing it through either name affects both. Copy deliberately; a shallow copy still shares nested objects.

### Small worked example

```python
from copy import deepcopy
raw = [{"amount": 100, "tags": ["imported"]}]
clean = deepcopy(raw)
clean[0]["tags"].append("validated")
assert raw[0]["tags"] == ["imported"]
```

The assertions show the expected result. [Run this example](../practice/examples/q02.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** Finance wants both the original transaction extract and a cleaned working version.

**Why I use this:** Preserve the original and choose a copy strategy appropriate for nested data.

**What I validate:** Confirm cleaning one version does not alter the retained original.

**Business value:** Maintain a reliable audit trail for reconciliation.

**Interview-ready response**

> “I would preserve the original and choose a copy strategy appropriate for nested data. I would confirm cleaning one version does not alter the retained original. This would help the business maintain a reliable audit trail for reconciliation.”

</details>

---

<a id="py-03"></a>
## PY-03 · Fresh defaults for every call

**Interview question**

Why can a list default cause records to leak between function calls?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

Default expressions are evaluated when the function is defined. A default list is therefore shared by calls that omit the argument. Use None, then create a new list inside the function. This keeps independent runs independent.

### Small worked example

```python
def reject(row, issues=None):
    if issues is None:
        issues = []
    issues.append(row)
    return issues
assert reject("A") == ["A"]
assert reject("B") == ["B"]
```

The assertions show the expected result. [Run this example](../practice/examples/q03.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A validation helper accumulates rejected rows from separate clients.

**Why I use this:** Create a fresh exception collection for each run unless the caller deliberately supplies one.

**What I validate:** Call the helper twice and confirm the second run contains only its own exceptions.

**Business value:** Prevent one client's rejected records appearing in another client's report.

**Interview-ready response**

> “I would create a fresh exception collection for each run unless the caller deliberately supplies one. I would call the helper twice and confirm the second run contains only its own exceptions. This would help the business prevent one client's rejected records appearing in another client's report.”

</details>

---

<a id="py-04"></a>
## PY-04 · Choosing a list or a lazy expression

**Interview question**

When would you build a list instead of a generator expression?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

A list stores all results and supports indexing and repeated iteration. A generator expression produces results as requested and is consumed once. It can avoid storing every result, but the input and each generated value still occupy memory. Choose based on how the result will be used.

### Small worked example

```python
orders = [{"status": "paid", "amount": 120}, {"status": "pending", "amount": 50}]
revenue = sum(o["amount"] for o in orders if o["status"] == "paid")
assert revenue == 120
```

The assertions show the expected result. [Run this example](../practice/examples/q04.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** Operations needs only the total of paid orders from a large incoming stream.

**Why I use this:** Feed a generator of eligible amounts into sum instead of storing another full list.

**What I validate:** Check eligibility and reconcile the total against a small hand-worked sample.

**Business value:** Reduce avoidable memory use while preserving the revenue definition.

**Interview-ready response**

> “I would feed a generator of eligible amounts into sum instead of storing another full list. I would check eligibility and reconcile the total against a small hand-worked sample. This would help the business reduce avoidable memory use while preserving the revenue definition.”

</details>

---

<a id="py-05"></a>
## PY-05 · Dictionary and set comprehensions

**Interview question**

How can comprehensions build a lookup or a unique collection?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

A dictionary comprehension builds key-value pairs; a set comprehension builds distinct values. Repeated dictionary keys overwrite earlier values, so validate uniqueness first when duplicates indicate an error. `:=` can reuse an intermediate calculation, but clarity is more valuable than a shorter line.

### Small worked example

```python
rows = [{"id": 1, "tier": "Gold", "city": "Thane"}, {"id": 2, "tier": "Silver", "city": "Thane"}]
assert len({r["id"] for r in rows}) == len(rows)
tiers = {r["id"]: r["tier"] for r in rows}
cities = {r["city"] for r in rows}
assert tiers[2] == "Silver" and cities == {"Thane"}
```

The assertions show the expected result. [Run this example](../practice/examples/q05.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** CRM needs a lookup of approved customer tiers and a list of distinct cities.

**Why I use this:** Build the lookup only after checking unique customer IDs; normalise cities under an agreed rule.

**What I validate:** Test duplicate IDs and city spelling variations.

**Business value:** Speed up enrichment without silently overwriting customer records.

**Interview-ready response**

> “I would build the lookup only after checking unique customer IDs; normalise cities under an agreed rule. I would test duplicate IDs and city spelling variations. This would help the business speed up enrichment without silently overwriting customer records.”

</details>

---

<a id="py-06"></a>
## PY-06 · Flexible arguments and clear signatures

**Interview question**

What do *args, **kwargs, / and a bare * mean in a function signature?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

`*args` collects extra positional arguments and `**kwargs` collects extra keyword arguments. At a call site, * and ** unpack collections. Parameters before / are positional-only; parameters after a bare * are keyword-only. Use an explicit signature when it makes business-rule choices easier to understand.

### Small worked example

```python
def revenue(amounts, /, *, refund_amount=0):
    return sum(amounts) - refund_amount
assert revenue([100, 200], refund_amount=20) == 280
```

The assertions show the expected result. [Run this example](../practice/examples/q06.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A reporting helper must make its refund-inclusion rule visible to every caller.

**Why I use this:** Require the refund option as a keyword rather than an unexplained positional boolean.

**What I validate:** Test the default policy and an explicit alternative.

**Business value:** Reduce accidental inconsistencies between reports.

**Interview-ready response**

> “I would require the refund option as a keyword rather than an unexplained positional boolean. I would test the default policy and an explicit alternative. This would help the business reduce accidental inconsistencies between reports.”

</details>

---

<a id="py-07"></a>
## PY-07 · Lambda functions and captured variables

**Interview question**

When is a lambda useful, and what is the late-binding trap?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

A lambda defines a small single-expression function. It fits a short sorting key; use def for named rules needing documentation. Closures normally look up captured variables when called, not when created. Bind a loop value deliberately when each callback needs its own value.

### Small worked example

```python
invoices = [{"id": 2, "days": 10}, {"id": 1, "days": 10}, {"id": 3, "days": 20}]
queue = sorted(invoices, key=lambda r: (-r["days"], r["id"]))
assert [r["id"] for r in queue] == [3, 1, 2]
fns = [lambda threshold=t: threshold for t in (10, 20)]
assert [f() for f in fns] == [10, 20]
```

The assertions show the expected result. [Run this example](../practice/examples/q07.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** Collections wants invoices ordered by overdue days, with invoice ID breaking ties.

**Why I use this:** Use a simple sorting key and name more complex prioritisation rules.

**What I validate:** Test tied priorities and, for generated callbacks, verify each captured threshold.

**Business value:** Give agents a consistent, explainable work queue.

**Interview-ready response**

> “I would use a simple sorting key and name more complex prioritisation rules. I would test tied priorities and, for generated callbacks, verify each captured threshold. This would help the business give agents a consistent, explainable work queue.”

</details>

---

<a id="py-08"></a>
## PY-08 · Truthiness without losing valid zeros

**Interview question**

What does if value test, and when is it too broad?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

False, None, numeric zero and empty built-in containers are falsy. User-defined types can customise truth testing. `if value` is useful for emptiness but cannot distinguish missing data from a valid zero. pandas objects often have ambiguous truth values; use explicit checks appropriate to the object.

### Small worked example

```python
def label_sales(value):
    if value is None:
        return "unknown"
    return "zero" if value == 0 else "recorded"
assert label_sales(None) == "unknown"
assert label_sales(0) == "zero"
```

The assertions show the expected result. [Run this example](../practice/examples/q08.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A product can have zero sales or an unavailable sales value.

**Why I use this:** Separate None from zero and label each condition appropriately.

**What I validate:** Test zero, positive values, None and empty input.

**Business value:** Avoid reporting unknown sales as confirmed no sales.

**Interview-ready response**

> “I would separate None from zero and label each condition appropriately. I would test zero, positive values, None and empty input. This would help the business avoid reporting unknown sales as confirmed no sales.”

</details>

---

<a id="py-09"></a>
## PY-09 · Business identity, equality and hashing

**Interview question**

How are object identity, equality and hashability related?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

Identity describes one object; equality describes the type's comparison rule. Hashable objects need a stable hash during their lifetime, and equal objects must have equal hashes. A class defining __eq__ without a suitable __hash__ usually becomes unhashable. That is often correct for mutable value objects; you do not always need to add a hash.

### Small worked example

```python
a = ("CRM", "C001")
b = tuple(["CRM", "C001"])
assert a == b and hash(a) == hash(b)
assert len({a, b}) == 1
```

The assertions show the expected result. [Run this example](../practice/examples/q09.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** Customer records from two extracts must be compared by an agreed business key.

**Why I use this:** Use an immutable customer identifier for sets and lookups instead of object memory identity.

**What I validate:** Confirm equal keys collapse and distinct customers stay separate.

**Business value:** Reconcile customers consistently across files.

**Interview-ready response**

> “I would use an immutable customer identifier for sets and lookups instead of object memory identity. I would confirm equal keys collapse and distinct customers stay separate. This would help the business reconcile customers consistently across files.”

</details>

---

<a id="py-10"></a>
## PY-10 · Assignment expressions

**Interview question**

What does := do, and when does it improve readability?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

`:=` assigns a value within an expression, making it available immediately. It can avoid repeating a calculation in a condition or comprehension. It is not a replacement for ordinary assignment, and a separate line is often easier to debug.

### Small worked example

```python
orders = [{"gross": 100, "refund": 20}, {"gross": 60, "refund": 10}]
net_values = [net for o in orders if (net := o["gross"] - o["refund"]) > 50]
assert net_values == [80]
```

The assertions show the expected result. [Run this example](../practice/examples/q10.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** An order review needs only records whose calculated net value is above a threshold.

**Why I use this:** Calculate net value once and retain it for the qualifying result.

**What I validate:** Check values exactly at the boundary and confirm the calculation is not repeated.

**Business value:** Apply one consistent eligibility rule.

**Interview-ready response**

> “I would calculate net value once and retain it for the qualifying result. I would check values exactly at the boundary and confirm the calculation is not repeated. This would help the business apply one consistent eligibility rule.”

</details>

---
