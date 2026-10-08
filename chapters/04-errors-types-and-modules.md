# 🔴 Errors, types and modules
[← Study hub](../README.md) · [Cheat sheet](../CHEAT_SHEET.md) · [Practice](../practice/README.md)

> [!TIP]
> Attempt the question aloud before expanding the answer. Each business case is hypothetical; describe it as “I would” unless it reflects work you actually did.

<a id="py-31"></a>
## PY-31 · Checking first or handling failure

**Interview question**

How do EAFP and LBYL affect error handling?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

LBYL checks before an operation; EAFP attempts the operation and handles a specific failure. Choose the clearer approach for expected failure frequency and available guarantees. EAFP is not automatically atomic or race-free: an external resource can change during the operation, and compound business updates still need proper concurrency controls.

### Small worked example

```python
def required_amount(row):
    try:
        return row["amount"]
    except KeyError as exc:
        raise ValueError("Missing required amount") from exc
assert required_amount({"amount": 0}) == 0
try:
    required_amount({})
except ValueError as exc:
    assert isinstance(exc.__cause__, KeyError)
else:
    raise AssertionError("Missing field accepted")
```

The assertions show the expected result. [Run this example](../practice/examples/q31.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A supplier row may omit a required amount field.

**Why I use this:** Attempt the required lookup and handle KeyError as a clear data-quality exception.

**What I validate:** Test missing fields separately from invalid amounts and unexpected programming errors.

**Business value:** Produce actionable exceptions without silently accepting incomplete data.

**Interview-ready response**

> “I would attempt the required lookup and handle KeyError as a clear data-quality exception. I would test missing fields separately from invalid amounts and unexpected programming errors. This would help the business produce actionable exceptions without silently accepting incomplete data.”

</details>

---

<a id="py-32"></a>
## PY-32 · The try statement lifecycle

**Interview question**

What do except, else and finally do?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

except handles matching exceptions from try. else runs after try succeeds, keeping follow-on work outside that handler. finally normally runs as control leaves the construct, including return or exception paths. Abrupt process termination is an exception to the usual cleanup expectation. Avoid returning from finally because it can hide failures.

### Small worked example

```python
events = []
try:
    amount = int("100")
except ValueError:
    events.append("invalid")
else:
    events.append("success")
finally:
    events.append("cleanup")
assert amount == 100 and events == ["success", "cleanup"]
```

The assertions show the expected result. [Run this example](../practice/examples/q32.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** An automated import must record success only after parsing, and always release its local resource.

**Why I use this:** Keep success handling in else and cleanup in finally or a context manager.

**What I validate:** Check both successful and failing runs release resources.

**Business value:** Avoid misleading success messages and resource leaks.

**Interview-ready response**

> “I would keep success handling in else and cleanup in finally or a context manager. I would check both successful and failing runs release resources. This would help the business avoid misleading success messages and resource leaks.”

</details>

---

<a id="py-33"></a>
## PY-33 · Business-specific exceptions

**Interview question**

When would you define your own exception class?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

Use a custom Exception subclass when callers need to distinguish an expected domain failure, such as invalid input, from other failures. Choose meaningful names and include safe context. Do not catch BaseException broadly and accidentally suppress interrupts or shutdown.

### Small worked example

```python
class UnsupportedCurrencyError(Exception):
    pass
def validate_currency(value):
    if value not in {"INR", "USD"}:
        raise UnsupportedCurrencyError(value)
    return value
assert validate_currency("INR") == "INR"
try:
    validate_currency("XYZ")
except UnsupportedCurrencyError:
    pass
else:
    raise AssertionError("Unsupported currency accepted")
```

The assertions show the expected result. [Run this example](../practice/examples/q33.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A payment reconciliation rejects records with an unsupported currency.

**Why I use this:** Raise a dedicated error that the workflow can route to a currency exception queue.

**What I validate:** Confirm supported currencies pass and unrelated failures are not swallowed.

**Business value:** Make exception ownership and follow-up clear.

**Interview-ready response**

> “I would raise a dedicated error that the workflow can route to a currency exception queue. I would confirm supported currencies pass and unrelated failures are not swallowed. This would help the business make exception ownership and follow-up clear.”

</details>

---

<a id="py-34"></a>
## PY-34 · Preserving the cause of failure

**Interview question**

What does raise NewError from original_error communicate?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

Explicit chaining records the original error as __cause__, giving both a useful domain message and diagnostic detail. from None suppresses the displayed implicit context, but does not erase all internal context. Translate exceptions deliberately rather than replacing every failure with a vague message.

### Small worked example

```python
class ImportValidationError(Exception):
    pass
def parse_amount(value):
    try:
        return int(value)
    except ValueError as exc:
        raise ImportValidationError("Amount must be an integer") from exc
try:
    parse_amount("unknown")
except ImportValidationError as exc:
    assert isinstance(exc.__cause__, ValueError)
else:
    raise AssertionError("Invalid amount accepted")
```

The assertions show the expected result. [Run this example](../practice/examples/q34.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** An import fails to parse a supplier amount and needs a business-readable error.

**Why I use this:** Raise an import validation error while preserving the parsing failure as its cause.

**What I validate:** Check the reported message and inspect the cause for support diagnosis.

**Business value:** Help the business understand the issue without losing technical evidence.

**Interview-ready response**

> “I would raise an import validation error while preserving the parsing failure as its cause. I would check the reported message and inspect the cause for support diagnosis. This would help the business help the business understand the issue without losing technical evidence.”

</details>

---

<a id="py-35"></a>
## PY-35 · Handling multiple failures

**Interview question**

Why do ExceptionGroup and except* exist?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

Python 3.11+ can package several related exceptions in an ExceptionGroup. except* handles matching members, while unhandled members continue propagating. This helps with concurrent operations where more than one failure can arise. Keep partial-success policy explicit instead of discarding failed work.

### Small worked example

```python
handled = []
try:
    raise ExceptionGroup("validation", [ValueError("bad amount"), TypeError("bad type")])
except* ValueError as group:
    handled.append(("value", len(group.exceptions)))
except* TypeError as group:
    handled.append(("type", len(group.exceptions)))
assert handled == [("value", 1), ("type", 1)]
```

The assertions show the expected result. [Run this example](../practice/examples/q35.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** Several source validations fail during the same reporting run.

**Why I use this:** Separate data-validation issues from other failures and report all relevant exceptions.

**What I validate:** Check mixed error types and ensure no unhandled category silently disappears.

**Business value:** Give source owners a complete remediation list.

**Interview-ready response**

> “I would separate data-validation issues from other failures and report all relevant exceptions. I would check mixed error types and ensure no unhandled category silently disappears. This would help the business give source owners a complete remediation list.”

</details>

---

<a id="py-36"></a>
## PY-36 · Nullable type hints

**Interview question**

Does Optional[int] mean the argument may be omitted?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

Optional[int] means int or None, equivalent to int | None in Python 3.10+. It does not mean a parameter can be omitted; a default controls that. Type annotations support static checking but do not enforce values at runtime unless additional validation is used.

### Small worked example

```python
def renewal_label(days: int | None) -> str:
    return "unknown" if days is None else f"{days} days"
assert renewal_label(None) == "unknown"
assert renewal_label(0) == "0 days"
```

The assertions show the expected result. [Run this example](../practice/examples/q36.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A churn model input has a renewal date that may genuinely be unknown.

**Why I use this:** Represent missingness explicitly and separately define whether callers must provide the field.

**What I validate:** Test a real value, None and an omitted required argument.

**Business value:** Avoid confusing unknown data with an optional input requirement.

**Interview-ready response**

> “I would represent missingness explicitly and separately define whether callers must provide the field. I would test a real value, None and an omitted required argument. This would help the business avoid confusing unknown data with an optional input requirement.”

</details>

---

<a id="py-37"></a>
## PY-37 · Union types and normalisation

**Interview question**

What does int | str express in a type annotation?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

It expresses a value that can be either type, equivalent to Union[int, str] for this case. It does not convert incoming values. When source systems use different representations, validate and normalise deliberately; avoid broad unions that leave every consumer guessing.

### Small worked example

```python
def normalise_id(value: int | str) -> str:
    return str(value).strip()
assert normalise_id(12) == "12"
assert normalise_id("0012") == "0012"
```

The assertions show the expected result. [Run this example](../practice/examples/q37.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** Two systems supply customer IDs as integers and strings.

**Why I use this:** Agree a canonical ID representation while preserving meaningful leading zeros.

**What I validate:** Check integer IDs, numeric strings and identifiers such as 0012.

**Business value:** Make joins predictable without damaging business identifiers.

**Interview-ready response**

> “I would agree a canonical ID representation while preserving meaningful leading zeros. I would check integer IDs, numeric strings and identifiers such as 0012. This would help the business make joins predictable without damaging business identifiers.”

</details>

---

<a id="py-38"></a>
## PY-38 · Protocols for interchangeable providers

**Interview question**

How can a Protocol describe an adapter without requiring inheritance?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

A Protocol declares the methods and attributes a static checker expects. Another class can satisfy the shape without inheriting from it. @runtime_checkable offers limited runtime presence checks, not full signature or data validation. Integration tests still need to verify business behaviour.

### Small worked example

```python
from typing import Protocol
class AmountProvider(Protocol):
    def amounts(self) -> list[int]: ...
class FixtureProvider:
    def amounts(self) -> list[int]:
        return [100, 150]
def revenue(provider: AmountProvider) -> int:
    return sum(provider.amounts())
assert revenue(FixtureProvider()) == 250
```

The assertions show the expected result. [Run this example](../practice/examples/q38.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A monthly report should accept a CSV adapter today and a database adapter later.

**Why I use this:** Define the expected provider interface and keep the report independent of its implementation.

**What I validate:** Check equivalent results and required fields with fixture providers.

**Business value:** Change providers without rewriting the report.

**Interview-ready response**

> “I would define the expected provider interface and keep the report independent of its implementation. I would check equivalent results and required fields with fixture providers. This would help the business change providers without rewriting the report.”

</details>

---

<a id="py-39"></a>
## PY-39 · Safe script entry points

**Interview question**

Why put execution code behind if __name__ == "__main__"?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

When a module runs as the main program, __name__ is "__main__"; importing it normally gives its module name. The guard keeps script entry code from running on import. Other top-level code still runs when imported, so keep unrelated work and side effects out of module scope.

### Small worked example

```python
def revenue(values):
    return sum(values)
def main():
    assert revenue([100, 200]) == 300
if __name__ == "__main__":
    main()
```

The assertions show the expected result. [Run this example](../practice/examples/q39.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A notebook needs to reuse a revenue function without starting the scheduled export.

**Why I use this:** Put the export workflow in main and guard its invocation.

**What I validate:** Import the module in a fresh process and check no export starts.

**Business value:** Make reusable calculations safe to import.

**Interview-ready response**

> “I would put the export workflow in main and guard its invocation. I would import the module in a fresh process and check no export starts. This would help the business make reusable calculations safe to import.”

</details>

---

<a id="py-40"></a>
## PY-40 · Imports and package structure

**Interview question**

When do absolute and relative imports make sense?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

Absolute imports name the package path; relative imports locate modules within the current package. Relative imports need package context, often supplied by python -m package.module. Circular dependencies may require moving shared definitions into a separate module. A deferred import can help some cases but does not fix every design problem.

### Small worked example

```python
# Standard-library absolute import; package examples are described in the answer.
from decimal import Decimal
assert Decimal("10.50") + Decimal("2.25") == Decimal("12.75")
```

The assertions show the expected result. [Run this example](../practice/examples/q40.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A reporting project splits readers, validation and metrics into reusable modules.

**Why I use this:** Define a clear dependency direction and put common contracts in a shared module.

**What I validate:** Run the package entry point and import modules independently.

**Business value:** Keep extensions maintainable and avoid fragile import order.

**Interview-ready response**

> “I would define a clear dependency direction and put common contracts in a shared module. I would run the package entry point and import modules independently. This would help the business keep extensions maintainable and avoid fragile import order.”

</details>

---
