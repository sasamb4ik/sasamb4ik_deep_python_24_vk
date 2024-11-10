import asyncio
import aiohttp
import argparse
import os


async def fetch(session, url, semaphore):
    async with semaphore:
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.text()
                print(
                    f"Захватили URL: {url} - длина составляет {len(data)} "
                    f"символов"
                    )
        except Exception as e:
            print(f"URL: {url} - Ошибка: {e}")


async def main(concurrency, file_path='urls.txt'):
    if not os.path.isfile(file_path):
        print(f"Файл {file_path} не найден.")
        return

    with open(file_path, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]

    print(
        f"Начали обработку {len(urls)} URL-адресов"
        f" {concurrency}"
        )
    semaphore = asyncio.Semaphore(concurrency)

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url, semaphore) for url in urls]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Асинхронная обкачка "
                    "URL-адресов."
        )
    parser.add_argument(
        '-c', '--concurrency', type=int, default=10,
        help="Количество одновременных запросов"
        )
    args = parser.parse_args()

    asyncio.run(main(args.concurrency))
