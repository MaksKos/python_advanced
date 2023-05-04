# pylint: disable=missing-docstring

import asyncio
import pytest
from unittest.mock import AsyncMock
from unittest import mock, IsolatedAsyncioTestCase
import fetcher


"""
@pytest.fixture()
def mock_fetch_url(mocker):
    async_mock = AsyncMock()
    mocker.patch('fetcher.fetch_url', side_effect=async_mock)
    return async_mock

@pytest.mark.asyncio
async def test_worker(mock_fetch_url: AsyncMock):
    
    queue = asyncio.Queue()
    await queue.put('url1')
    mock_fetch_url.return_value = None
    worker = asyncio.create_task(fetcher.async_worker(queue))
    await queue.join()
    worker.cancel()
    print(mock_fetch_url.await_args())


@pytest.fixture()
def mock_async_worker(mocker):
    pass

"""

class TestClienr(IsolatedAsyncioTestCase):

    async def test_worker(self):
        mock_queue = AsyncMock()
        mock_queue.get.side_effect = 'url1', 'url2'
        mock_fetch = AsyncMock()
        #queue = asyncio.Queue()
        #await queue.put('url1')
        #await queue.put('url2')

        with mock.patch('fetcher.fetch_url', mock_fetch) as mf:
            worker = asyncio.create_task(fetcher.async_worker(mock_queue))
            await asyncio.sleep(0.1)
        worker.cancel()

        print(mock_fetch.call_args_list)
        print(mock_fetch.mock_queue.task_done)

                  


