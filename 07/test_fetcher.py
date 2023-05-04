# pylint: disable=missing-docstring

import asyncio
from unittest.mock import AsyncMock, MagicMock
from unittest import mock, IsolatedAsyncioTestCase
import fetcher


class AsynFile:

    def __init__(self, urls) -> None:
        self.urls = iter(urls)

    def __aiter__(self):
        return self

    async def __anext__(self):

        try:
            url = next(self.urls)
        except StopIteration as exep:
            raise StopAsyncIteration from exep

        return url


class TestClienr(IsolatedAsyncioTestCase):

    async def test_worker(self):
        mock_fetch = AsyncMock()
        queue = asyncio.Queue()
        await queue.put('url1')
        await queue.put('url2')

        with mock.patch('fetcher.fetch_url', mock_fetch):
            worker = asyncio.create_task(fetcher.async_worker(queue))
            await asyncio.sleep(0.1)
        worker.cancel()

        call = [mock.call('url1'), mock.call('url2')]
        self.assertEqual(mock_fetch.call_args_list, call)

    @mock.patch('fetcher.print')
    @mock.patch('aiohttp.ClientSession.get')
    async def test_fetcher(self, mock_get, _):

        urls = ['url1', 'url2', 'url3']
        mock_get.return_value.__aenter__.return_value.status = 200
        for url in urls:
            await fetcher.fetch_url(url)

        call = [mock.call(url) for url in urls]
        self.assertEqual(mock_get.call_args_list, call)
        self.assertEqual(fetcher.COUNT, 3)

    @mock.patch('asyncio.Queue')
    @mock.patch('aiofiles.open')
    @mock.patch('asyncio.create_task')
    async def test_main(self, mock_task, mock_file, mock_qu):

        queue = AsyncMock()
        urls = ['url1', 'url2', 'url3']
        mock_qu.return_value = queue
        mock_file.return_value.__aenter__.return_value = AsynFile(urls)
        n_workers = 5
        file_name = 'urls.txt'

        with mock.patch('fetcher.async_worker', MagicMock()) as work:
            await fetcher.main(n_workers, file_name)

        call = [mock.call(work(queue))]*n_workers
        self.assertEqual(mock_task.call_args_list, call)

        self.assertEqual(mock_qu.call_count, 1)
        self.assertEqual(queue.join.call_count, 1)
        self.assertEqual(mock_task().cancel.call_count, n_workers)

        calls = [mock.call(url) for url in urls]
        self.assertEqual(queue.put.call_args_list, calls)
        self.assertEqual(mock_file.call_args, mock.call(file_name, mode='r'))
