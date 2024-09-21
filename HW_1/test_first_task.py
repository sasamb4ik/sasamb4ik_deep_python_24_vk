import unittest
from first_task import SomeModel, predict_message_mood


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
        self._assert_raises_message(
            "Hello,mynameisgleb",
            self.invalid_format_msg
        )
        self._assert_raises_message("    ", self.invalid_format_msg)
        self.assertAlmostEqual(self.model.predict("aeiou"), 1.0)
        self.assertAlmostEqual(self.model.predict("HeLLo"), 0.4)
        self.assertAlmostEqual(self.model.predict("rhythm"), 0.0)
        self.assertAlmostEqual(self.model.predict("gle"), 0.333)
        self.assertAlmostEqual(self.model.predict("mimmughffrf"), 0.182)

    def test_predict_message_mood(self):
        self.assertEqual(predict_message_mood("aeiou"), "отл")
        self.assertEqual(predict_message_mood("HeLLo"), "норм")
        self.assertEqual(predict_message_mood("rhytm"), "неуд")
        self.assertEqual(predict_message_mood("gle"), "норм")
        self.assertEqual(predict_message_mood("mimmughffrf"), "неуд")
        self.assertEqual(predict_message_mood("aaaiffoooooeeeffeuuuuu"), "отл")
