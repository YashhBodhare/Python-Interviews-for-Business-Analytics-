class Report:
    def __init__(self, reader):
        self.reader = reader
    def revenue(self):
        return sum(self.reader())
report = Report(lambda: [100, 200])
assert report.revenue() == 300
