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
