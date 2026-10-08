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
