# pylint: disable=missing-docstring

import argparse
import asyncio
import aiohttp
import aiofiles

COUNT = 0


async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            global COUNT
            COUNT += 1
            assert resp.status == 200
            print(f'get url ({COUNT=}): {url}', end='')


async def async_worker(queue):
    while True:
        url = await queue.get()
        try:
            await fetch_url(url)
        except aiohttp.ClientError as error:
            print(error)
            continue
        finally:
            queue.task_done()


async def main(n_workers: int, file_name: str):

    queue = asyncio.Queue(n_workers)

    workers = [
        asyncio.create_task(async_worker(queue))
        for _ in range(n_workers)
    ]

    async with aiofiles.open(file_name, mode='r') as file:
        async for url in file:
            if not url:
                break
            await queue.put(url)

    await queue.join()

    for worker in workers:
        worker.cancel()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-c')
    parser.add_argument('file')
    args = parser.parse_args()
    asyncio.run(main(int(args.c), args.file))
