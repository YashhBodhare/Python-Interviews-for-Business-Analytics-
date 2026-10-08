def choose_candidate(workload, async_library=False):
    if workload == "cpu":
        return "processes to benchmark"
    return "asyncio" if async_library else "threads"
assert choose_candidate("io", True) == "asyncio"
assert choose_candidate("cpu") == "processes to benchmark"
