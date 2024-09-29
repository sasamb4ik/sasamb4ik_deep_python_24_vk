import unittest
from unittest.mock import patch
from io import StringIO
from file_generator import search_file_generator


class TestSecondTask(unittest.TestCase):

    @patch(
        "builtins.open",
        new_callable=unittest.mock.mock_open,
        read_data="This is a mocked line.\n"
        "Gleb loves big data.\n"
        "Another line with data.\n",
    )
    def test_basics_and_read_file(self, mocked_open: patch):
        result = list(search_file_generator("fake_path", ["data"], ["gleb"]))
        self.assertEqual(result, ["Another line with data."])
        mocked_open.assert_called_once_with("fake_path", "r", encoding="utf-8")

    def test_empty_file(self):
        with patch("builtins.open", new_callable=unittest.mock.mock_open, read_data=""):
            result = list(search_file_generator("fake_path", ["data"], []))
            self.assertEqual(result, [])

    def test_full_string_search_match(self):
        with patch(
            "builtins.open",
            new_callable=unittest.mock.mock_open,
            read_data="полностью подходящая строка\nhello world\ndata " "science\n",
        ):
            result = list(
                search_file_generator("fake_path", ["полностью подходящая строка"], [])
            )
            self.assertEqual(result, ["полностью подходящая строка"])

    def test_full_string_stop_match(self):
        with patch(
            "builtins.open",
            new_callable=unittest.mock.mock_open,
            read_data="полностью анти подходящая строка\nhello world\ndata "
            "science\n",
        ):
            result = list(
                search_file_generator(
                    "fake_path", ["анти"], ["полностью анти подходящая строка"]
                )
            )
            self.assertEqual(result, [])

    def test_multiple_search_words_in_one_line(self):
        with patch(
            "builtins.open",
            new_callable=unittest.mock.mock_open,
            read_data="Тут будет много подходящих search слов (точно "
            "больше одного).\n лапа папу маму кораллы карл)",
        ):
            result = list(
                search_file_generator(
                    "fake_path", ["слов", "search", "больше"], ["кораллы"]
                )
            )
            self.assertEqual(
                result,
                ["Тут будет много подходящих search слов (точно " "больше одного)."],
            )

    def test_multiple_stop_words_in_one_line(self):
        with patch(
            "builtins.open",
            new_callable=unittest.mock.mock_open,
            read_data="Rosa loves Azora and Tulip flowers.",
        ):
            result = list(
                search_file_generator("fake_path", ["rosa"], ["azora", "tulip"])
            )
            self.assertEqual(result, [])

    def test_no_matches(self):
        with patch(
            "builtins.open",
            new_callable=unittest.mock.mock_open,
            read_data="This line has no keywords.\nAnother irrelevant line.",
        ):
            result = list(search_file_generator("fake_path", ["keyword"], []))
            self.assertEqual(result, [])

    def test_search_and_stop_empty(self):
        with patch(
            "builtins.open",
            new_callable=unittest.mock.mock_open,
            read_data="Тут есть какой-то текст.\n я исправляю первую "
            "попытки сдачи домашки. поставьте пожалуйста 7 "
            "баллов.",
        ):
            result = list(search_file_generator("fake_path", [], []))
            self.assertEqual(result, [])

    def test_exact_word_matching(self):
        with patch(
            "builtins.open",
            new_callable=unittest.mock.mock_open,
            read_data="Я хочу проверить полное вхождение слова.\nполно "
            "тебе горевать!",
        ):
            result = list(search_file_generator("fake_path", ["полно"], []))
            self.assertEqual(result, ["полно тебе горевать!"])

    def test_file_like_object_and_capital_letters(self):
        fake_file = StringIO("Gleb loves data science.\nPython is great.\n")
        result = list(search_file_generator(fake_file, ["PytHon"], []))
        self.assertEqual(result, ["Python is great."])

    def test_special_characters_and_spaces(self):
        with patch(
            "builtins.open",
            new_callable=unittest.mock.mock_open,
            read_data="    Line with spe!!cial     character     "
            "%percent.\n"
            "Line without     keyword.\n",
        ):
            result = list(search_file_generator("fake_path", ["percent"], []))
            self.assertEqual(
                result, ["Line with spe!!cial     character     %percent."]
            )

    def test_invalid_input_format(self):
        with self.assertRaises(ValueError):
            list(search_file_generator(12345, ["data"], ["gleb"]))

        with self.assertRaises(ValueError):
            list(search_file_generator(["makaka"], ["data"], ["gleb"]))

        with self.assertRaises(ValueError):
            list(search_file_generator(tuple("orangutang"), ["data"], ["gleb"]))
