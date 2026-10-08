import asyncio
async def source_total():
    await asyncio.sleep(0)
    return 300
async def main():
    return await source_total()
assert asyncio.run(main()) == 300
