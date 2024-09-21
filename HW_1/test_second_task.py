import unittest
from unittest.mock import patch

from second_task import search_file_generator


class TestSecondTask(unittest.TestCase):

    @patch(
        'builtins.open', new_callable=unittest.mock.mock_open,
        read_data='This is a mocked line.\nGleb loves big data.\nAnother line with data.\n'
    )
    def test_basics_and_read_file(self, mocked_open: patch):
        result = list(search_file_generator('fake_path', ['data'], ['gleb']))
        self.assertEqual(result, ['Another line with data.'])
        mocked_open.assert_called_once_with('fake_path', 'r', encoding='utf-8')

    @patch(
        'builtins.open', new_callable=unittest.mock.mock_open, read_data=''
    )
    def test_empty_file(self, mocked_open: patch):
        result = list(search_file_generator('fake_path', ['data'], []))
        self.assertEqual(result, [])

    @patch(
        'builtins.open', new_callable=unittest.mock.mock_open,
        read_data='This line has no keywords.\nAnother irrelevant line.'
    )
    def test_no_matches(self, mocked_open: patch):
        result = list(search_file_generator('fake_path', ['keyword'], []))
        self.assertEqual(result, [])

    @patch(
        'builtins.open', new_callable=unittest.mock.mock_open,
        read_data='Line with special character %percent.\nLine without '
                  'keyword.\n'
    )
    def test_special_characters(self, mocked_open: patch):
        result = list(search_file_generator('fake_path', ['percent'], []))
        self.assertEqual(result, ['Line with special character %percent.'])
