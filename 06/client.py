import socket
import threading
import argparse


class RequestThread(threading.Thread):
    def __init__(self, url, host, port):
        super().__init__()
        self.url = url
        self.host = host
        self.port = port

    def run(self):
        sock = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM
        )
        try:
            sock.connect((self.host, self.port))
            sock.sendall(self.url.encode("utf-8"))
            response = sock.recv(4096).decode("utf-8")
            print(response)
        except ConnectionError as e:
            print(f"Ошибка при подключении к серверу: {e}")
        finally:
            sock.close()


class ClientThread(threading.Thread):
    def __init__(self, urls, host, port):
        super().__init__()
        self.urls = urls
        self.host = host
        self.port = port

    def run(self):
        threads = []
        for url in self.urls:
            thread = RequestThread(url, self.host, self.port)
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()


def read_urls_in_chunks(file_path, chunk_size):
    with open(file_path, "r", encoding="utf-8") as file:
        while True:
            chunk = [line.strip() for line in file.readlines(chunk_size)]
            if not chunk:
                break
            yield chunk


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", type=str, default="localhost", help="Хост сервера"
    )
    parser.add_argument("--port", type=int, default=65432, help="Порт сервера")
    parser.add_argument(
        "--urls_file", type=str, required=True, help="Файл с URL"
    )
    parser.add_argument(
        "--num_threads", type=int, default=4, help="Кол-во " "потоков клиента"
    )
    parser.add_argument(
        "--chunk_size",
        type=int,
        default=1024,
        help="Размер чтения файла (в строках)",
    )
    args = parser.parse_args()

    threads = []
    for chunk in read_urls_in_chunks(args.urls_file, args.chunk_size):
        thread = ClientThread(chunk, args.host, args.port)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
