#checking async things

import asyncio

async def task1():
    await asyncio.sleep(1)
    return "Task 1 Done"

async def task2():
    await asyncio.sleep(2)
    return "Task 2 Done"

async def main():
    tasks = [task1(), task2()]
    results = await asyncio.gather(*tasks)
    print(results)

asyncio.run(main())