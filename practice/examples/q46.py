import asyncio
async def main():
    try:
        async with asyncio.timeout(0.01):
            await asyncio.sleep(1)
    except TimeoutError:
        return "source unavailable"
    raise AssertionError("Expected timeout")
assert asyncio.run(main()) == "source unavailable"
