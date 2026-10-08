# 🔵 Concurrency and runtime choices
[← Study hub](../README.md) · [Cheat sheet](../CHEAT_SHEET.md) · [Practice](../practice/README.md)

> [!TIP]
> Attempt the question aloud before expanding the answer. Each business case is hypothetical; describe it as “I would” unless it reflects work you actually did.

<a id="py-41"></a>
## PY-41 · The GIL and workload limits

**Interview question**

What does the GIL imply for conventional CPython threads?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

In a conventional GIL-enabled CPython build, only one thread executes Python bytecode at a time. Threads can still overlap waiting on I/O, and some native libraries release the GIL for computation. This is not a business-level thread-safety guarantee. Optional free-threaded builds change the execution model; label the build before making performance claims.

### Small worked example

```python
import sys
check = getattr(sys, "_is_gil_enabled", None)
gil_status = check() if check else "not exposed by this runtime"
assert gil_status in (True, False, "not exposed by this runtime")
```

The assertions show the expected result. [Run this example](../practice/examples/q41.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A report reads several independent supplier sources before doing CPU-heavy Python calculations.

**Why I use this:** Separate I/O time from computation time before choosing a concurrency model.

**What I validate:** Measure each stage and compare representative workloads.

**Business value:** Choose an approach that improves the actual bottleneck.

**Interview-ready response**

> “I would separate I/O time from computation time before choosing a concurrency model. I would measure each stage and compare representative workloads. This would help the business choose an approach that improves the actual bottleneck.”

</details>

---

<a id="py-42"></a>
## PY-42 · Choosing threads, processes or asyncio

**Interview question**

How would you select a concurrency approach for a business workflow?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

Start with the workload and library support. Threads often fit blocking I/O; asyncio fits cooperative async I/O; processes can help independent CPU-heavy Python work in a GIL-enabled build. Native vectorised libraries, free-threaded builds, data-transfer costs and task size can change the best choice. Benchmark and bound concurrency.

### Small worked example

```python
def choose_candidate(workload, async_library=False):
    if workload == "cpu":
        return "processes to benchmark"
    return "asyncio" if async_library else "threads"
assert choose_candidate("io", True) == "asyncio"
assert choose_candidate("cpu") == "processes to benchmark"
```

The assertions show the expected result. [Run this example](../practice/examples/q42.py).

> [!NOTE]
> This snippet illustrates a decision rule, not a performance benchmark.

### 🧑‍💼 Business Analyst scenario

**Business need:** A nightly pipeline downloads independent sources, then scores a large customer dataset.

**Why I use this:** Consider bounded I/O concurrency and a separately benchmarked calculation stage.

**What I validate:** Check provider limits, result consistency, runtime and peak resource use.

**Business value:** Meet the delivery deadline without overwhelming dependencies.

**Interview-ready response**

> “I would consider bounded I/O concurrency and a separately benchmarked calculation stage. I would check provider limits, result consistency, runtime and peak resource use. This would help the business meet the delivery deadline without overwhelming dependencies.”

</details>

---

<a id="py-43"></a>
## PY-43 · Coroutines and await

**Interview question**

What happens when you call an async function?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

Calling async def returns a coroutine object; its body runs when awaited or scheduled. await waits for an awaitable and can let the event loop run other ready work if it suspends. Not every await suspends. Blocking work inside a coroutine can block the whole event-loop thread.

### Small worked example

```python
import asyncio
async def source_total():
    await asyncio.sleep(0)
    return 300
async def main():
    return await source_total()
assert asyncio.run(main()) == 300
```

The assertions show the expected result. [Run this example](../practice/examples/q43.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A dashboard refresh should wait for a source response without blocking other async requests.

**Why I use this:** Use an async-capable client and keep synchronous blocking work off the event-loop path.

**What I validate:** Check scheduling and the result for both success and failure.

**Business value:** Keep independent I/O work responsive.

**Interview-ready response**

> “I would use an async-capable client and keep synchronous blocking work off the event-loop path. I would check scheduling and the result for both success and failure. This would help the business keep independent I/O work responsive.”

</details>

---

<a id="py-44"></a>
## PY-44 · Starting an async program

**Interview question**

When is asyncio.run appropriate?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

asyncio.run manages an event loop for a top-level async program and returns its result. It cannot run in a thread that already has a running event loop. In environments such as many notebooks, use top-level await instead. Avoid repeatedly starting loops inside a larger async workflow.

### Small worked example

```python
import asyncio
async def collect():
    return {"source_rows": 3}
if __name__ == "__main__":
    assert asyncio.run(collect()) == {"source_rows": 3}
```

The assertions show the expected result. [Run this example](../practice/examples/q44.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A standalone reporting script must launch its async collection step.

**Why I use this:** Use one program entry point; adapt notebook usage to the existing loop.

**What I validate:** Check execution in the target environment and resource cleanup.

**Business value:** Avoid event-loop conflicts during deployment or exploration.

**Interview-ready response**

> “I would use one program entry point; adapt notebook usage to the existing loop. I would check execution in the target environment and resource cleanup. This would help the business avoid event-loop conflicts during deployment or exploration.”

</details>

---

<a id="py-45"></a>
## PY-45 · Concurrent tasks and failure policy

**Interview question**

How do gather and TaskGroup differ?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

gather returns results in input order. By default its first exception propagates while sibling awaitables are not automatically cancelled solely because of that failure. TaskGroup manages task lifetimes and normally cancels siblings after a non-cancellation failure, then reports grouped failures. Choose whether partial success is useful; cancellation does not undo external business effects.

### Small worked example

```python
import asyncio
async def fetch(value):
    await asyncio.sleep(0)
    return value
async def main():
    async with asyncio.TaskGroup() as group:
        first = group.create_task(fetch(100))
        second = group.create_task(fetch(200))
    return first.result() + second.result()
assert asyncio.run(main()) == 300
```

The assertions show the expected result. [Run this example](../practice/examples/q45.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A consolidated report needs complete data from every required source.

**Why I use this:** Use a structured task scope and define whether any failed source should prevent publication.

**What I validate:** Test all-success, one failure and cleanup; mark incomplete reports clearly.

**Business value:** Prevent partially loaded data from appearing as a complete report.

**Interview-ready response**

> “I would use a structured task scope and define whether any failed source should prevent publication. I would test all-success, one failure and cleanup; mark incomplete reports clearly. This would help the business prevent partially loaded data from appearing as a complete report.”

</details>

---

<a id="py-46"></a>
## PY-46 · Timeouts and cancellation

**Interview question**

How do asyncio.timeout and wait_for limit waiting?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

asyncio.timeout provides a deadline scope; wait_for waits for a particular awaitable with a timeout. Both rely on cancellation, which is cooperative rather than a hard process kill. Cleanup can extend elapsed time, and remote operations may already have taken effect. Do not swallow CancelledError unintentionally.

### Small worked example

```python
import asyncio
async def main():
    try:
        async with asyncio.timeout(0.01):
            await asyncio.sleep(1)
    except TimeoutError:
        return "source unavailable"
    raise AssertionError("Expected timeout")
assert asyncio.run(main()) == "source unavailable"
```

The assertions show the expected result. [Run this example](../practice/examples/q46.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** A source call must not make the reporting workflow wait indefinitely.

**Why I use this:** Set a justified deadline and define the fallback, retry and freshness message.

**What I validate:** Test timeout handling and confirm the report never silently substitutes a stale value.

**Business value:** Make delays visible and controlled.

**Interview-ready response**

> “I would set a justified deadline and define the fallback, retry and freshness message. I would test timeout handling and confirm the report never silently substitutes a stale value. This would help the business make delays visible and controlled.”

</details>

---

<a id="py-47"></a>
## PY-47 · Locks and shared invariants

**Interview question**

Why can a shared update still need a lock?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

A shared read-modify-write sequence is not guaranteed safe simply because a GIL exists. A lock coordinates cooperating threads around the relevant invariant. It does not automatically coordinate processes, database writers or other machines. Avoid relying on a specific bytecode count or incidental runtime behaviour.

### Small worked example

```python
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
```

The assertions show the expected result. [Run this example](../practice/examples/q47.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** Several worker threads add successful source counts to one run summary.

**Why I use this:** Protect the shared update or combine separate worker results without shared mutation.

**What I validate:** Run concurrent workers and reconcile the final count.

**Business value:** Avoid missing updates in operational totals.

**Interview-ready response**

> “I would protect the shared update or combine separate worker results without shared mutation. I would run concurrent workers and reconcile the final count. This would help the business avoid missing updates in operational totals.”

</details>

---

<a id="py-48"></a>
## PY-48 · Process pools for independent computation

**Interview question**

When could multiprocessing.Pool be a good fit?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

A process pool can distribute independent CPU-heavy work across processes. Account for start-up, serialisation and data-transfer overhead; tiny tasks may become slower. Use importable worker functions, an entry-point guard and a start method appropriate to the platform. Processes do not share ordinary Python objects automatically.

### Small worked example

```python
from multiprocessing import get_context
def squared(value):
    return value * value
if __name__ == "__main__":
    with get_context("spawn").Pool(2) as pool:
        results = pool.map(squared, [2, 3, 4])
    assert results == [4, 9, 16]
```

The assertions show the expected result. [Run this example](../practice/examples/q48.py).

> [!NOTE]
> Tiny inputs demonstrate correctness only; they do not justify multiprocessing on performance grounds.

### 🧑‍💼 Business Analyst scenario

**Business need:** A planning simulation evaluates many independent regional demand cases.

**Why I use this:** Benchmark batches of substantial independent calculations and preserve case IDs with results.

**What I validate:** Compare sequential and parallel outputs, startup costs and memory usage.

**Business value:** Shorten analysis time only when the workload justifies the overhead.

**Interview-ready response**

> “I would benchmark batches of substantial independent calculations and preserve case IDs with results. I would compare sequential and parallel outputs, startup costs and memory usage. This would help the business shorten analysis time only when the workload justifies the overhead.”

</details>

---

<a id="py-49"></a>
## PY-49 · Executors and futures

**Interview question**

What does concurrent.futures simplify?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

Executors provide a shared interface for submitting work to threads or processes. A Future represents a result or failure. map preserves input order; as_completed yields futures as they finish. Keep a mapping back to business IDs and handle exceptions explicitly. Availability of additional executor types depends on the Python version.

### Small worked example

```python
from concurrent.futures import ThreadPoolExecutor, as_completed
def fetch_total(supplier):
    return {"A": 100, "B": 200}[supplier]
with ThreadPoolExecutor(max_workers=2) as pool:
    pending = {pool.submit(fetch_total, s): s for s in ("A", "B")}
    totals = {pending[f]: f.result() for f in as_completed(pending)}
assert totals == {"A": 100, "B": 200}
```

The assertions show the expected result. [Run this example](../practice/examples/q49.py).

### 🧑‍💼 Business Analyst scenario

**Business need:** An analyst collects independent supplier totals and needs each result linked to its source.

**Why I use this:** Use futures with a supplier-ID mapping and set sensible concurrency limits.

**What I validate:** Check every supplier is accounted for, including failed requests.

**Business value:** Avoid attributing a result to the wrong source.

**Interview-ready response**

> “I would use futures with a supplier-ID mapping and set sensible concurrency limits. I would check every supplier is accounted for, including failed requests. This would help the business avoid attributing a result to the wrong source.”

</details>

---

<a id="py-50"></a>
## PY-50 · Optional free-threaded CPython

**Interview question**

What should you say about Python free-threaded builds in an interview?

<details>
<summary><strong>💡 Answer, example and BA scenario</strong></summary>

### Simple answer

CPython 3.13 introduced an experimental optional free-threaded build. Python 3.14 makes that optional build officially supported; it is still not the default. GIL-disabled threads can execute Python in parallel, but scaling is workload-dependent. Extension compatibility matters, and an incompatible extension may re-enable the GIL. Benchmark and retain explicit synchronisation; do not promise a fixed speedup or an adoption date.

### Small worked example

```python
import sysconfig
free_threaded_build = bool(sysconfig.get_config_var("Py_GIL_DISABLED"))
assert isinstance(free_threaded_build, bool)
```

The assertions show the expected result. [Run this example](../practice/examples/q50.py).

> [!NOTE]
> Build configuration and actual runtime GIL state are different checks. This example detects a build setting; it does not test parallel speedup.

### 🧑‍💼 Business Analyst scenario

**Business need:** A team is evaluating whether its CPU-heavy analysis can benefit from a different interpreter build.

**Why I use this:** Ask engineering to pilot the exact package stack and workload, with correct results as an acceptance criterion.

**What I validate:** Check the actual GIL state after imports, extension support, runtime, memory and shared-state safety.

**Business value:** Adopt only when measured benefits justify migration effort.

**Interview-ready response**

> “I would ask engineering to pilot the exact package stack and workload, with correct results as an acceptance criterion. I would check the actual GIL state after imports, extension support, runtime, memory and shared-state safety. This would help the business adopt only when measured benefits justify migration effort.”

</details>

---
