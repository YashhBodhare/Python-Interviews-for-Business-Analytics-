import sys
check = getattr(sys, "_is_gil_enabled", None)
gil_status = check() if check else "not exposed by this runtime"
assert gil_status in (True, False, "not exposed by this runtime")
