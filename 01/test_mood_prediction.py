import unittest
from unittest.mock import patch
from mood_prediction import SomeModel, predict_message_mood


class TestFirstTask(unittest.TestCase):

    def setUp(self):
        self.model = SomeModel()
        self.empty_str_msg = "Вы передали пустую строку."
        self.invalid_format_msg = (
            "Неверный входной формат строки. "
            "Строка должна состоять только из букв Unicode формата."
        )

    def test_count_vowels(self):
        self.assertEqual(self.model.count_vowels("hello"), 2)
        self.assertEqual(self.model.count_vowels("hELlo"), 2)
        self.assertEqual(self.model.count_vowels(""), 0)
        self.assertEqual(self.model.count_vowels("rhythm"), 0)
        self.assertEqual(self.model.count_vowels("aeiouAEIOU"), 10)
        self.assertEqual(self.model.count_vowels("Hello, world!"), 3)

    def _assert_raises_message(self, message, expected_message):
        with self.assertRaises(ValueError) as context:
            self.model.predict(message)
        self.assertEqual(str(context.exception), expected_message)

    @patch.object(SomeModel, "predict")
    def test_predict_message_mood(self, mock_predict):
        mock_predict.side_effect = [
            1.0,  # "aeiou"
            0.4,  # "HeLLo"
            0.0,  # "rhythm"
            0.333,  # "gle"
            0.182,  # "mimmughffrf"
            0.9,  # "aaaiffoooooeeeffeuuuuu"
        ]

        self.assertEqual(predict_message_mood("aeiou"), "отл")
        mock_predict.assert_called_with("aeiou")

        self.assertEqual(predict_message_mood("HeLLo"), "норм")
        mock_predict.assert_called_with("HeLLo")

        self.assertEqual(predict_message_mood("rhythm"), "неуд")
        mock_predict.assert_called_with("rhythm")

        self.assertEqual(predict_message_mood("gle"), "норм")
        mock_predict.assert_called_with("gle")

        self.assertEqual(predict_message_mood("mimmughffrf"), "неуд")
        mock_predict.assert_called_with("mimmughffrf")

        self.assertEqual(predict_message_mood("aaaiffoooooeeeffeuuuuu"), "отл")
        mock_predict.assert_called_with("aaaiffoooooeeeffeuuuuu")

        self.assertEqual(mock_predict.call_count, 6)

    @patch.object(SomeModel, "predict")
    def test_predict_message_mood_thresholds(self, mock_predict):
        mock_predict.side_effect = [
            0.182,
            0.182,
            0.182,
            0.0,
            0.0,
            0.4,
            0.333,
            0.333,
            0.333,
            0.33299,
            0.33299,
        ]

        self.assertEqual(
            predict_message_mood("mimmughffrf", 0.181, 0.183), "норм"
        )
        mock_predict.assert_called_with("mimmughffrf")

        self.assertEqual(
            predict_message_mood("mimmughffrf", 0.182, 0.183), "норм"
        )
        mock_predict.assert_called_with("mimmughffrf")

        self.assertEqual(
            predict_message_mood("mimmughffrf", 0.18201, 0.183), "неуд"
        )
        mock_predict.assert_called_with("mimmughffrf")

        self.assertEqual(predict_message_mood("rhythm", 0), "норм")
        mock_predict.assert_called_with("rhythm")

        self.assertEqual(predict_message_mood("rhythm", 0.05, 0.1), "неуд")
        mock_predict.assert_called_with("rhythm")

        self.assertEqual(predict_message_mood("HeLLo", 0.2, 0.3), "отл")
        mock_predict.assert_called_with("HeLLo")

        self.assertEqual(predict_message_mood("gle", 0.32, 0.332), "отл")
        mock_predict.assert_called_with("gle")

        self.assertEqual(predict_message_mood("gle", 0.32, 0.333), "норм")
        mock_predict.assert_called_with("gle")

        self.assertEqual(predict_message_mood("gle", 0.333, 0.333), "норм")
        mock_predict.assert_called_with("gle")

        self.assertEqual(predict_message_mood("gle", 0.332, 0.329999), "отл")
        mock_predict.assert_called_with("gle")

        self.assertEqual(predict_message_mood("gle", 0.33299, 0.333001), "норм")
        mock_predict.assert_called_with("gle")

        self.assertEqual(mock_predict.call_count, 11)
