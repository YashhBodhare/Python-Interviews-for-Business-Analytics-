def rows_from_batches(batches):
    for batch in batches:
        yield from batch
assert list(rows_from_batches([[101, 102], [], [103]])) == [101, 102, 103]
