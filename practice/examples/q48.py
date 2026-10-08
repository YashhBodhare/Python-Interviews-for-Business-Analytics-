from multiprocessing import get_context
def squared(value):
    return value * value
if __name__ == "__main__":
    with get_context("spawn").Pool(2) as pool:
        results = pool.map(squared, [2, 3, 4])
    assert results == [4, 9, 16]
