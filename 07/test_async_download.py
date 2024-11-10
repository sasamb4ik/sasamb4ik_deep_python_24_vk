import asyncio
import unittest
from unittest import mock
from unittest.mock import patch, mock_open
from aioresponses import aioresponses
import aiohttp

from async_download import fetch, main


class TestFetcher(unittest.IsolatedAsyncioTestCase):
    @aioresponses()
    async def test_fetch_success(self, mocked):
        url = "https://example.com"
        mock_response = "Mocked ответ"
        mocked.get(url, status=200, body=mock_response)

        semaphore = asyncio.Semaphore(10)
        async with aiohttp.ClientSession() as session:
            with patch('builtins.print') as mock_print:
                await fetch(session, url, semaphore)
                mock_print.assert_called_with(
                    f"Захватили URL: {url} - длина составляет {len(mock_response)} символов"
                )

    @aioresponses()
    async def test_fetch_failure(self, mocked):
        url = "https://example.com"
        mocked.get(url, exception=asyncio.TimeoutError())

        semaphore = asyncio.Semaphore(10)
        async with aiohttp.ClientSession() as session:
            with patch('builtins.print') as mock_print:
                await fetch(session, url, semaphore)
                args, _ = mock_print.call_args
                self.assertTrue(args[0].startswith(f"URL: {url} - Ошибка:"))

    @aioresponses()
    async def test_main_success(self, mocked):
        urls = ["https://example.com/page1", "https://example.com/page2"]
        mock_responses = {
            urls[0]: "Контент на первой странице",
            urls[1]: "Контент на второй странице"
        }

        for url, content in mock_responses.items():
            mocked.get(url, status=200, body=content)

        with patch('builtins.print') as mock_print:
            with patch('os.path.isfile', return_value=True):
                with patch(
                        'builtins.open', mock_open(read_data="\n".join(urls))
                        ):
                    await main(concurrency=2, file_path='urls.txt')

            expected_calls = [
                mock.call(f"Начали обработку {len(urls)} URL-адресов 2"),
                mock.call(
                    f"Захватили URL: {urls[0]} - длина составляет {len(mock_responses[urls[0]])} символов"
                    ),
                mock.call(
                    f"Захватили URL: {urls[1]} - длина составляет {len(mock_responses[urls[1]])} символов"
                    ),
            ]

            mock_print.assert_has_calls(expected_calls, any_order=False)

    async def test_main_empty_file(self):
        with patch('builtins.print') as mock_print:
            with patch('os.path.isfile', return_value=True):
                with patch('builtins.open', mock_open(read_data="")):
                    await main(concurrency=2, file_path='urls.txt')
                    mock_print.assert_any_call(
                        "Начали обработку 0 URL-адресов 2"
                        )

    async def test_main_file_not_found(self):
        with patch('builtins.print') as mock_print:
            with patch('os.path.isfile', return_value=False):
                await main(concurrency=2, file_path="non_existent_file.txt")
                mock_print.assert_called_with(
                    "Файл non_existent_file.txt не найден."
                    )


if __name__ == '__main__':
    unittest.main()
