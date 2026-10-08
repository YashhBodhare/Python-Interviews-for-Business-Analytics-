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
