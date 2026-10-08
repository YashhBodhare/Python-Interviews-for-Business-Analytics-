from concurrent.futures import ThreadPoolExecutor, as_completed
def fetch_total(supplier):
    return {"A": 100, "B": 200}[supplier]
with ThreadPoolExecutor(max_workers=2) as pool:
    pending = {pool.submit(fetch_total, s): s for s in ("A", "B")}
    totals = {pending[f]: f.result() for f in as_completed(pending)}
assert totals == {"A": 100, "B": 200}
