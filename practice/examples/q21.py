class ReportConfig:
    def __init__(self, currency):
        if currency not in {"INR", "USD"}:
            raise ValueError("Unsupported currency")
        self.currency = currency
assert ReportConfig("INR").currency == "INR"
