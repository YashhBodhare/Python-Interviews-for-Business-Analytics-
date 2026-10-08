class Base:
    pass
class Validation(Base):
    pass
class Logging(Base):
    pass
class Report(Validation, Logging):
    pass
assert [c.__name__ for c in Report.__mro__] == ["Report", "Validation", "Logging", "Base", "object"]
