from abc import ABC, abstractmethod
class Reader(ABC):
    @abstractmethod
    def read(self):
        raise NotImplementedError
class FixtureReader(Reader):
    def read(self):
        return [100, 200]
assert FixtureReader().read() == [100, 200]
