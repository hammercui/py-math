"""
show how to use async & await for asynchronous operation
"""
import asyncio
import time


async def download_file(url):
    print(f"Downloading {url}")
    await asyncio.sleep(1)  # simulating file download time
    print(f"Downloaded {url}")
    return url


async def gather():
    print(": test gather")
    tasks = [download_file("file_url_1"), download_file("file_url_2")]
    # * as unpacking arguments
    # gather return  aggregating results
    results = await asyncio.gather(*tasks)
    print(results, type(results))


async def sleep():
    print("single sleep")
    await asyncio.sleep(1)
    print("single sleep end")


async def task():
    print("create task")
    await asyncio.sleep(1)
    print("create task execute over")
    task = asyncio.create_task(sleep())
    print(task, type(task))
    await task

async def task_group():
    """
    only useful in 3.11
    :return:
    """
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(task())
        task2 = tg.create_task(task())
        print("asyncio.TaskGroup() over")
    print(f"finished at {time.strftime('%X')}")


async def do_io():
    print('io start')
    await asyncio.sleep(2)
    print('io end')


async def do_other_things():
    print('doing other things')


if __name__ == "__main__":
    # gather mode
    # asyncio.run(gather())
    #
    # asyncio.run(sleep())
    #
    # asyncio.run(task())
    # asyncio.run(task_group())

    loop = asyncio.get_event_loop()
    print(loop, type(loop))
    loop.create_task(do_other_things())
    loop.run_until_complete(do_io())
    loop.close()

    time.sleep(3)
