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
