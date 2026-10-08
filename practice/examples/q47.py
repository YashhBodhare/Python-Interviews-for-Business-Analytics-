from threading import Lock
from concurrent.futures import ThreadPoolExecutor
lock = Lock()
count = 0
def add(_):
    global count
    with lock:
        count += 1
with ThreadPoolExecutor(max_workers=4) as pool:
    list(pool.map(add, range(100)))
assert count == 100
