from dataclasses import dataclass, field
@dataclass
class ReportRecord:
    run_id: str
    warnings: list[str] = field(default_factory=list)
a = ReportRecord("A")
b = ReportRecord("B")
a.warnings.append("late source")
assert b.warnings == []
