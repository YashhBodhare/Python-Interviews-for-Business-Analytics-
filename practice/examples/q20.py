from functools import lru_cache
@lru_cache(maxsize=16)
def classification(product_id, rules_version):
    return "core" if product_id == "P01" else "other"
assert classification("P01", "v1") == "core"
classification("P01", "v1")
assert classification.cache_info().hits == 1
