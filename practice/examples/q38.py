from typing import Protocol
class AmountProvider(Protocol):
    def amounts(self) -> list[int]: ...
class FixtureProvider:
    def amounts(self) -> list[int]:
        return [100, 150]
def revenue(provider: AmountProvider) -> int:
    return sum(provider.amounts())
assert revenue(FixtureProvider()) == 250
