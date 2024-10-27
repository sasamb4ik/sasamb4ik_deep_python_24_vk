import socket
import threading
import requests
from collections import Counter
import re


class Worker(threading.Thread):
    def __init__(self, conn, addr, top_k, server):
        super().__init__()
        self.conn = conn
        self.addr = addr
        self.top_k = top_k
        self.server = server

    def run(self):
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
                    print(f"Обработано адресов: {self.server.processed_urls}")
        finally:
            self.conn.close()

    def fetch_and_process(self, url):
        try:
            response = requests.get(url)
            text = response.text
            words = re.findall(r"\w+", text.lower())
            counts = Counter(words)
            top = counts.most_common(self.top_k)
            return dict(top)
        except requests.RequestException as e:
            print(f"Ошибка при попыткп обработки адреса {url}: {e}")
            return {}


class Master(threading.Thread):
    def __init__(self, host, port, top_k):
        super().__init__()
        self.host = host
        self.port = port
        self.top_k = top_k
        self.processed_urls = 0
        self.lock = threading.Lock()
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        try:
            while True:
                conn, addr = self.server_socket.accept()
                print(f"Подключились к {addr}")

                worker = Worker(conn, addr, self.top_k, self)
                worker.start()
        finally:
            self.server_socket.close()


class ClientThread(threading.Thread):
    def __init__(self, urls, host, port):
        super().__init__()
        self.urls = urls
        self.host = host
        self.port = port

    def run(self):
        for url in self.urls:
            try:
                with socket.socket(
                    socket.AF_INET, socket.SOCK_STREAM
                ) as client_socket:
                    client_socket.connect((self.host, self.port))
                    client_socket.sendall(url.encode("utf-8"))

                    response = client_socket.recv(4096).decode("utf-8")
                    print(response)
            except ConnectionError as e:
                print(f"Ошибка при подключении к серверу: {e}")


def read_urls(file_path):
    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]


def run_client(num_threads, urls_file):
    urls = read_urls(urls_file)
    chunk_size = len(urls) // num_threads
    threads = []

    for i in range(num_threads):
        start_idx = i * chunk_size
        end_idx = None if i == num_threads - 1 else (i + 1) * chunk_size
        thread_urls = urls[start_idx:end_idx]
        thread = ClientThread(thread_urls, "localhost", 65432)
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
