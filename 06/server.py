import socket
import threading
from collections import Counter
import re
import requests
import argparse


class Worker(threading.Thread):
    def __init__(self, conn, addr, top_k, server, semaphore):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.top_k = top_k
        self.server = server
        self.semaphore = semaphore

    def run(self):
        with self.semaphore:
            try:
                while True:
                    url = self.conn.recv(1024).decode("utf-8")
                    if not url:
                        break
                    print(f"Воркер взял адрес: {url}")

                    top_words = self.fetch_and_process(url)
                    response = f"{url}: {top_words}"

                    self.conn.send(response.encode("utf-8"))
                    with self.server.lock:
                        self.server.processed_urls += 1
                        print(
                            f"Обработано адресов: {self.server.processed_urls}"
                        )
            finally:
                self.conn.close()

    def fetch_and_process(self, url):
        try:
            response = requests.get(url, timeout=10)
            text = response.text
            words = re.findall(r"\w+", text.lower())
            counts = Counter(words)
            top = counts.most_common(self.top_k)
            return dict(top)
        except requests.RequestException as e:
            print(f"Ошибка при попытке обработки адреса {url}: {e}")
            return {}


class Master(threading.Thread):
    def __init__(self, host, port, top_k, max_workers):
        super().__init__()
        self.host = host
        self.port = port
        self.top_k = top_k
        self.max_workers = max_workers
        self.processed_urls = 0
        self.lock = threading.Lock()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.semaphore = threading.Semaphore(max_workers)

    def run(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        try:
            while True:
                conn, addr = self.server_socket.accept()
                print(f"Подключились к {addr}")

                worker = Worker(conn, addr, self.top_k, self, self.semaphore)
                worker.start()
        finally:
            self.server_socket.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", type=str, default="localhost", help="Хост сервера"
    )
    parser.add_argument("--port", type=int, default=65432, help="Порт сервера")
    parser.add_argument(
        "--top_k", type=int, default=10, help="Кол-во " "популярных слов"
    )
    parser.add_argument(
        "--max_workers",
        type=int,
        default=5,
        help="Макс количество одновременных воркеров",
    )
    args = parser.parse_args()

    server = Master(args.host, args.port, args.top_k, args.max_workers)
    server.start()
    server.join()
