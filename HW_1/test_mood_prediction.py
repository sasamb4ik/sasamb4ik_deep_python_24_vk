import unittest
from unittest.mock import patch, Mock
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

    def test_predict(self):
        self._assert_raises_message("", self.empty_str_msg)
        self._assert_raises_message("Hello123", self.invalid_format_msg)
        self._assert_raises_message("Hello,mynameisgleb", self.invalid_format_msg)
        self._assert_raises_message("    ", self.invalid_format_msg)
        self.assertAlmostEqual(self.model.predict("aeiou"), 1.0)
        self.assertAlmostEqual(self.model.predict("HeLLo"), 0.4)
        self.assertAlmostEqual(self.model.predict("rhythm"), 0.0)
        self.assertAlmostEqual(self.model.predict("gle"), 0.333)
        self.assertAlmostEqual(self.model.predict("mimmughffrf"), 0.182)

    @patch.object(SomeModel, "predict")
    def test_predict_message_mood(self, mock_predict):
        mock_predict.side_effect = [1.0, 0.4, 0.0, 0.333, 0.182, 0.9]

        self.assertEqual(predict_message_mood("aeiou"), "отл")
        self.assertEqual(predict_message_mood("HeLLo"), "норм")
        self.assertEqual(predict_message_mood("rhytm"), "неуд")
        self.assertEqual(predict_message_mood("gle"), "норм")
        self.assertEqual(predict_message_mood("mimmughffrf"), "неуд")
        self.assertEqual(predict_message_mood("aaaiffoooooeeeffeuuuuu"), "отл")

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

        self.assertEqual(predict_message_mood("mimmughffrf", 0.181, 0.183), "норм")
        self.assertEqual(predict_message_mood("mimmughffrf", 0.182, 0.183), "норм")
        self.assertEqual(predict_message_mood("mimmughffrf", 0.18201, 0.183), "неуд")
        self.assertEqual(predict_message_mood("rhytm", 0), "норм")
        self.assertEqual(predict_message_mood("rhytm", 0.05, 0.1), "неуд")
        self.assertEqual(predict_message_mood("HeLLo", 0.2, 0.3), "отл")
        self.assertEqual(predict_message_mood("gle", 0.32, 0.332), "отл")
        self.assertEqual(predict_message_mood("gle", 0.32, 0.333), "норм")
        self.assertEqual(predict_message_mood("gle", 0.333, 0.333), "норм")
        self.assertEqual(predict_message_mood("gle", 0.332, 0.329999), "отл")
        self.assertEqual(predict_message_mood("gle", 0.33299, 0.333001), "норм")

        self.assertEqual(mock_predict.call_count, 11)
