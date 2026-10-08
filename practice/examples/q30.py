class Amounts:
    def __init__(self, gross, refund):
        self.gross, self.refund = gross, refund
    @property
    def net(self):
        return self.gross - self.refund
assert Amounts(100, 20).net == 80
