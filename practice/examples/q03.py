def reject(row, issues=None):
    if issues is None:
        issues = []
    issues.append(row)
    return issues
assert reject("A") == ["A"]
assert reject("B") == ["B"]
