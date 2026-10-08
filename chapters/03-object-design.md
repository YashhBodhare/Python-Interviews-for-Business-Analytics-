# 🟠 Objects and reusable design
[← Study hub](../README.md) · [Cheat sheet](../CHEAT_SHEET.md) · [Practice](../practice/README.md)

> [!TIP]
> Attempt the question aloud before expanding the answer. Each business case is hypothetical; describe it as “I would” unless it reflects work you actually did.

<a id="py-21"></a>
## PY-21 · Creating and initialising objects

**Interview question**

How do __new__ and __init__ differ?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

__new__ creates or returns the instance; __init__ initialises it when appropriate. Most ordinary classes need only __init__. Custom __new__ is useful for specialised construction, including immutable subclasses. __init__ must return None. Do not add construction complexity without a requirement.

### Small worked example

```python
class ReportConfig:
    def __init__(self, currency):
        if currency not in {"INR", "USD"}:
            raise ValueError("Unsupported currency")
        self.currency = currency
assert ReportConfig("INR").currency == "INR"
```

The assertions show the expected result. [Run this example](../practice/examples/q21.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A report configuration must start with a valid reporting currency.

**Why I use this:** Initialise the configuration with the required fields and reject unsupported currencies.

**What I validate:** Check valid and invalid inputs before any calculations start.

**Business value:** Prevent reports being run with an unintended currency.

**Interview-ready response**

> “I would initialise the configuration with the required fields and reject unsupported currencies. I would check valid and invalid inputs before any calculations start. This would help the business prevent reports being run with an unintended currency.”

</details>

---

<a id="py-22"></a>
## PY-22 · Method resolution and super

**Interview question**

How does Python decide which inherited method to use?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

The method resolution order, or MRO, determines the lookup sequence. Python uses C3 linearisation; inspect Class.__mro__ rather than assuming a simple traversal. super() follows that order, not necessarily one fixed parent. Cooperative inheritance requires compatible method signatures and consistent use of super.

### Small worked example

```python
class Base:
    pass
class Validation(Base):
    pass
class Logging(Base):
    pass
class Report(Validation, Logging):
    pass
assert [c.__name__ for c in Report.__mro__] == ["Report", "Validation", "Logging", "Base", "object"]
```

The assertions show the expected result. [Run this example](../practice/examples/q22.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A shared reporting component combines validation and logging behaviour through inheritance.

**Why I use this:** Ask engineering to make the execution order visible and confirm each required step runs once.

**What I validate:** Inspect MRO and trace behaviour in a diamond-shaped hierarchy.

**Business value:** Avoid skipped or duplicated processing steps.

**Interview-ready response**

> “I would ask engineering to make the execution order visible and confirm each required step runs once. I would inspect MRO and trace behaviour in a diamond-shaped hierarchy. This would help the business avoid skipped or duplicated processing steps.”

</details>

---

<a id="py-23"></a>
## PY-23 · Instance, class and static methods

**Interview question**

How would you choose between the three method forms?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

An instance method receives self for instance-specific work. A class method receives cls and can implement an alternative constructor that respects subclasses. A static method receives neither automatically and groups a helper with the class. It can still access explicitly supplied objects; it simply has no implicit instance or class parameter.

### Small worked example

```python
class Order:
    def __init__(self, amount):
        self.amount = amount
    @classmethod
    def from_dict(cls, row):
        return cls(row["amount"])
    @staticmethod
    def valid_amount(amount):
        return amount >= 0
    def net(self, refund):
        return self.amount - refund
assert Order.from_dict({"amount": 100}).net(20) == 80
assert Order.valid_amount(0)
```

The assertions show the expected result. [Run this example](../practice/examples/q23.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** An order record arrives as a dictionary and needs a consistent object representation.

**Why I use this:** Use a class method for the conversion and an instance method for the order calculation.

**What I validate:** Check parsing, required fields and the calculated amount.

**Business value:** Standardise how incoming records become usable business objects.

**Interview-ready response**

> “I would use a class method for the conversion and an instance method for the order calculation. I would check parsing, required fields and the calculated amount. This would help the business standardise how incoming records become usable business objects.”

</details>

---

<a id="py-24"></a>
## PY-24 · Slots and object layout

**Interview question**

What can __slots__ change about instances?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

__slots__ declares attribute slots and can avoid a per-instance __dict__, reducing memory in suitable classes. It can restrict extra attributes, but inheritance or including __dict__ changes that behaviour. Weak-reference support may require __weakref__. Measure savings on the actual workload.

### Small worked example

```python
class Event:
    __slots__ = ("event_id", "amount")
    def __init__(self, event_id, amount):
        self.event_id, self.amount = event_id, amount
event = Event(1, 100)
assert event.amount == 100 and not hasattr(event, "__dict__")
```

The assertions show the expected result. [Run this example](../practice/examples/q24.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A prototype loads many small event objects and approaches its memory limit.

**Why I use this:** Compare a slotted representation with the current model after confirming required fields.

**What I validate:** Measure memory and check serialisation, inheritance and missing-field handling.

**Business value:** Choose a representation that fits the processing environment.

**Interview-ready response**

> “I would compare a slotted representation with the current model after confirming required fields. I would measure memory and check serialisation, inheritance and missing-field handling. This would help the business choose a representation that fits the processing environment.”

</details>

---

<a id="py-25"></a>
## PY-25 · Readable and diagnostic representations

**Interview question**

What roles do __str__ and __repr__ serve?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

__str__ supplies a readable display; __repr__ supplies a useful diagnostic representation. A reconstructable repr can be helpful, but it is not always possible or appropriate. Do not expose personal data, passwords or tokens in either representation, and do not eval untrusted representations.

### Small worked example

```python
class ReportRun:
    def __init__(self, run_id):
        self.run_id = run_id
    def __str__(self):
        return f"Report run {self.run_id}"
    def __repr__(self):
        return f"ReportRun(run_id={self.run_id!r})"
run = ReportRun("R01")
assert str(run) == "Report run R01"
assert repr(run) == "ReportRun(run_id='R01')"
```

The assertions show the expected result. [Run this example](../practice/examples/q25.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** Support needs a useful report-run label without exposing customer details.

**Why I use this:** Keep a friendly status display and a diagnostic representation limited to safe identifiers.

**What I validate:** Inspect logs for helpful context and sensitive-data leakage.

**Business value:** Support diagnosis while minimising unnecessary data exposure.

**Interview-ready response**

> “I would keep a friendly status display and a diagnostic representation limited to safe identifiers. I would inspect logs for helpful context and sensitive-data leakage. This would help the business support diagnosis while minimising unnecessary data exposure.”

</details>

---

<a id="py-26"></a>
## PY-26 · Dataclasses and safe field defaults

**Interview question**

What does @dataclass generate, and what does frozen=True guarantee?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

A dataclass generates methods such as __init__, __repr__ and __eq__ from declared fields. default_factory creates separate mutable defaults. frozen=True blocks ordinary field reassignment; it does not make nested lists immutable. A generated hash can still fail if participating fields are unhashable. Use immutable field values when a truly stable value key is needed.

### Small worked example

```python
from dataclasses import dataclass, field
@dataclass
class ReportRecord:
    run_id: str
    warnings: list[str] = field(default_factory=list)
a = ReportRecord("A")
b = ReportRecord("B")
a.warnings.append("late source")
assert b.warnings == []
```

The assertions show the expected result. [Run this example](../practice/examples/q26.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A report record contains a run ID and a list of validation warnings.

**Why I use this:** Use a dataclass with a fresh warning list per record; avoid assuming frozen makes that list immutable.

**What I validate:** Check two records do not share warnings and evaluate hashability separately.

**Business value:** Keep report metadata clear and prevent warning leakage.

**Interview-ready response**

> “I would use a dataclass with a fresh warning list per record; avoid assuming frozen makes that list immutable. I would check two records do not share warnings and evaluate hashability separately. This would help the business keep report metadata clear and prevent warning leakage.”

</details>

---

<a id="py-27"></a>
## PY-27 · Composition and inheritance

**Interview question**

When would you prefer composition over subclassing?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

Composition gives an object a collaborator to use; inheritance models a subtype that must honour the parent contract. Composition is often easier when a data source or calculation needs to be swapped. Inheritance remains useful for genuine substitutable relationships. Choose from the requirement, not a universal rule.

### Small worked example

```python
class Report:
    def __init__(self, reader):
        self.reader = reader
    def revenue(self):
        return sum(self.reader())
report = Report(lambda: [100, 200])
assert report.revenue() == 300
```

The assertions show the expected result. [Run this example](../practice/examples/q27.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A revenue report should work with either a database reader or an approved file reader.

**Why I use this:** Supply the reader as a dependency instead of creating a subclass for every combination.

**What I validate:** Run the same report against both adapters using equivalent fixture data.

**Business value:** Change data access without duplicating KPI logic.

**Interview-ready response**

> “I would supply the reader as a dependency instead of creating a subclass for every combination. I would run the same report against both adapters using equivalent fixture data. This would help the business change data access without duplicating KPI logic.”

</details>

---

<a id="py-28"></a>
## PY-28 · Abstract classes and structural contracts

**Interview question**

How do an abstract base class and a Protocol differ?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

An ABC can require abstract methods before a concrete subclass is instantiated. ABCs also support mechanisms such as virtual registration, so recognition is not exclusively explicit inheritance. A Protocol describes a structural interface for static checking. Type hints alone do not validate runtime data or enforce every signature.

### Small worked example

```python
from abc import ABC, abstractmethod
class Reader(ABC):
    @abstractmethod
    def read(self):
        raise NotImplementedError
class FixtureReader(Reader):
    def read(self):
        return [100, 200]
assert FixtureReader().read() == [100, 200]
```

The assertions show the expected result. [Run this example](../practice/examples/q28.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** Several teams provide different source readers for a common report.

**Why I use this:** Define the reader contract and decide whether runtime abstract-method enforcement or structural typing fits the integration.

**What I validate:** Test that each implementation returns the agreed schema, not just that a method exists.

**Business value:** Integrate sources without ambiguous expectations.

**Interview-ready response**

> “I would define the reader contract and decide whether runtime abstract-method enforcement or structural typing fits the integration. I would test that each implementation returns the agreed schema, not just that a method exists. This would help the business integrate sources without ambiguous expectations.”

</details>

---

<a id="py-29"></a>
## PY-29 · Stable hashes and deduplication

**Interview question**

What must be true when equal objects are used in a set or dictionary?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

Objects that compare equal must have equal hashes. The hash must remain stable while the object is used as a key. Unequal objects can share a hash; that is a collision, not a correctness violation. Keep mutable equality fields out of hash keys or use an immutable business key.

### Small worked example

```python
from dataclasses import dataclass
@dataclass(frozen=True)
class TransactionKey:
    source: str
    transaction_id: str
a = TransactionKey("ERP", "T1")
b = TransactionKey("ERP", "T1")
c = TransactionKey("CRM", "T1")
assert a == b and hash(a) == hash(b)
assert len({a, b, c}) == 2
```

The assertions show the expected result. [Run this example](../practice/examples/q29.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A transaction reconciliation should identify repeated source transaction IDs.

**Why I use this:** Represent identity with immutable source-system and transaction-ID fields.

**What I validate:** Check the same ID in different systems and duplicates within one system.

**Business value:** Detect true duplicates without conflating unrelated transactions.

**Interview-ready response**

> “I would represent identity with immutable source-system and transaction-ID fields. I would check the same ID in different systems and duplicates within one system. This would help the business detect true duplicates without conflating unrelated transactions.”

</details>

---

<a id="py-30"></a>
## PY-30 · Properties for computed values

**Interview question**

When would a property be clearer than a method or raw attribute?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

A property exposes a getter as attribute-style access and can add validation through a setter. It fits a cheap derived value or an attribute with a stable public interface. Avoid hiding expensive queries, unexpected mutations or remote calls behind an apparently simple attribute.

### Small worked example

```python
class Amounts:
    def __init__(self, gross, refund):
        self.gross, self.refund = gross, refund
    @property
    def net(self):
        return self.gross - self.refund
assert Amounts(100, 20).net == 80
```

The assertions show the expected result. [Run this example](../practice/examples/q30.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A finance record needs a net amount derived from gross and refunds.

**Why I use this:** Expose the derived amount without storing another value that can drift out of sync.

**What I validate:** Test zero refunds, full refunds and the agreed policy for refunds exceeding gross.

**Business value:** Keep gross, refund and net values consistent.

**Interview-ready response**

> “I would expose the derived amount without storing another value that can drift out of sync. I would test zero refunds, full refunds and the agreed policy for refunds exceeding gross. This would help the business keep gross, refund and net values consistent.”

</details>

---
