import unittest
from unittest.mock import patch, MagicMock
import threading
import client
import server
import tempfile
import os


class TestClientServer(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(
            delete=False, mode="w", encoding="utf-8"
        )
        self.temp_file.writelines(
            ["http://example.com\n", "http://test.com\n"]
        )
        self.temp_file.close()

    def tearDown(self):
        os.unlink(self.temp_file.name)

    @patch("requests.get")
    def test_worker_fetch_and_process(self, mock_get):
        mock_response = MagicMock()
        mock_response.text = "hello world hello"
        mock_get.return_value = mock_response

        worker = server.Worker(None, None, 2, None, None)
        result = worker.fetch_and_process("http://example.com")
        self.assertEqual(result, {"hello": 2, "world": 1})

    @patch("socket.socket")
    def test_client_thread(self, mock_socket):
        mock_conn = MagicMock()
        mock_socket.return_value = mock_conn
        mock_conn.recv.return_value = b"http://example.com: {'hello': 2}"

        urls = ["http://example.com"]
        thread = client.ClientThread(urls, "localhost", 65432)
        thread.run()

        mock_conn.connect.assert_called_with(("localhost", 65432))

        mock_conn.sendall.assert_called_with(urls[0].encode("utf-8"))

        mock_conn.recv.assert_called()

    @patch("socket.socket")
    def test_server_worker(self, mock_socket):
        mock_conn = MagicMock()
        mock_conn.recv.side_effect = [b"http://example.com", b""]
        mock_socket.return_value = mock_conn

        server_instance = server.Master("localhost", 65432, 2, 2)
        server_instance.lock = threading.Lock()
        worker = server.Worker(
            mock_conn,
            ("127.0.0.1", 12345),
            2,
            server_instance,
            threading.Semaphore(2),
        )

        with patch.object(
            worker, "fetch_and_process", return_value={"hello": 2}
        ):
            worker.run()
            mock_conn.send.assert_called_with(
                b"http://example.com: {'hello': 2}"
            )

    def test_read_urls_in_chunks(self):
        chunk_size = 1
        chunks = list(
            client.read_urls_in_chunks(self.temp_file.name, chunk_size)
        )
        self.assertEqual(len(chunks), 2)
        self.assertEqual(chunks[0], ["http://example.com"])
        self.assertEqual(chunks[1], ["http://test.com"])

    def test_semaphore_limit(self):
        semaphore = threading.Semaphore(2)
        results = list()

        def task(idx):
            with semaphore:
                results.append(idx)

        threads = [threading.Thread(target=task, args=(i,)) for i in range(5)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(len(results), 5)


if __name__ == "__main__":
    unittest.main()
