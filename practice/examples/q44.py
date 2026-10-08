import asyncio
async def collect():
    return {"source_rows": 3}
if __name__ == "__main__":
    assert asyncio.run(collect()) == {"source_rows": 3}
