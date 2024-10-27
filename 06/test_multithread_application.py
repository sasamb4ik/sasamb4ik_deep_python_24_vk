import unittest
from unittest.mock import patch, MagicMock, mock_open
from multithreading_application import (
    read_urls,
    run_client,
    ClientThread,
    Worker,
)
import requests


class TestMultithreadingApplication(unittest.TestCase):

    def test_read_urls(self):
        mock_file_content = "http://example.com\nhttp://example.org\n"
        expected_output = ["http://example.com", "http://example.org"]

        with patch("builtins.open", mock_open(read_data=mock_file_content)):
            result = read_urls("urls.txt")
            self.assertEqual(result, expected_output)

    def test_read_urls_empty_file(self):
        expected_output = []

        with patch("builtins.open", mock_open(read_data="")):
            result = read_urls("urls.txt")
            self.assertEqual(result, expected_output)

    @patch("multithreading_application.ClientThread.run")
    def test_run_client(self, mock_run):
        urls_list = ["http://example.com", "http://example.org"]
        with patch(
            "multithreading_application.read_urls", return_value=urls_list
        ):
            run_client(2, "urls.txt")

        self.assertEqual(mock_run.call_count, 2)

    @patch("socket.socket")
    def test_client_thread(self, mock_socket):
        mock_instance = mock_socket.return_value.__enter__.return_value
        urls_list = ["http://example.com", "http://example.org"]

        client_thread = ClientThread(urls_list, "localhost", 65432)
        client_thread.start()
        client_thread.join()

        self.assertEqual(mock_instance.connect.call_count, len(urls_list))
        self.assertEqual(mock_instance.sendall.call_count, len(urls_list))

    @patch("requests.get", side_effect=requests.exceptions.ConnectionError)
    def test_worker_fetch_and_process_connection_error(self, mock_get):
        conn = MagicMock()
        server = MagicMock()

        worker = Worker(conn, "localhost", 2, server)
        top_words = worker.fetch_and_process("http://example.com")

        self.assertEqual(top_words, {})
