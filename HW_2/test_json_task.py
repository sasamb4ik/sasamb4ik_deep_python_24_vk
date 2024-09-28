import unittest
from json_task import process_json, remove_punctuation
from unittest.mock import patch, Mock


class TestProcessJson(unittest.TestCase):

    def setUp(self):
        self.mocked_json = {
            "gleb!": "This is a test!",
            "hello)": "More tests, here!"
        }
        self.mocked_json_string = '{"gleb!": "This is a test!", "hello)": "More tests, here!"}'
        self.required_keys = ["gleb", "hello"]
        self.mocked_callback = Mock()

    def test_remove_punctuation(self):
        self.assertEqual(remove_punctuation("Hello, World!"), "Hello World")
        self.assertEqual(
            remove_punctuation("выаываы!!яыаэээ?"), "выаываыяыаэээ"
            )
        self.assertEqual(remove_punctuation("п"), "п")
        self.assertEqual(remove_punctuation(""), "")
        self.assertEqual(
            remove_punctuation("я ща,с си?жу и #$@*&^ дома!шку"),
            "я щас сижу и  домашку"
            )

    @patch('first_task.json.loads')
    def test_process_json_with_matches(self, mocked_json_loads):
        mocked_json_loads.return_value = self.mocked_json

        tokens = ["this", "tests"]

        process_json(
            self.mocked_json_string, self.required_keys, tokens, self.mocked_callback
            )

        mocked_json_loads.assert_called_once_with(self.mocked_json_string)

        self.mocked_callback.assert_any_call("gleb!", "this")
        self.mocked_callback.assert_any_call("hello)", "tests")
        self.assertEqual(self.mocked_callback.call_count, 2)

    @patch('first_task.json.loads')
    def test_process_json_no_matches(self, mocked_json_loads):
        mocked_json_loads.return_value = self.mocked_json

        tokens = ["mango", "apple"]

        process_json(self.mocked_json_string, self.required_keys, tokens, self.mocked_callback)

        mocked_json_loads.assert_called_once_with(self.mocked_json_string)

        self.mocked_callback.assert_not_called()

