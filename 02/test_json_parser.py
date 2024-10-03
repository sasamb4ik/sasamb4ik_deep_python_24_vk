import unittest
from unittest.mock import Mock
from json_parser import process_json, remove_punctuation


class TestProcessJson(unittest.TestCase):

    def test_remove_punctuation(self):
        self.assertEqual(remove_punctuation("Hello, World!"), "Hello World")
        self.assertEqual(remove_punctuation("выаываы!!яыаэээ?"), "выаываыяыаэээ")
        self.assertEqual(
            remove_punctuation("С этой строкой ничего не " "произойдёт"),
            "С этой строкой ничего не " "произойдёт",
        )
        self.assertEqual(remove_punctuation("п"), "п")
        self.assertEqual(remove_punctuation("@"), "")
        self.assertEqual(remove_punctuation(""), "")
        self.assertEqual(remove_punctuation("растут% цветы&"), "растут цветы")
        self.assertEqual(
            remove_punctuation("я ща,с си?жу и #$@*&^   дома!шку"),
            "я щас сижу и    домашку",
        )

    def test_process_json_basic(self):
        json_str = (
            '{"Воскресенье": "Привет", "работа": "машинлернер", '
            '"город": '
            '"Москва"}'
        )
        required_keys = ["Воскресенье", "работа"]
        tokens = ["Привет", "машинлернер"]

        mock_callback = Mock()

        process_json(json_str, required_keys, tokens, mock_callback)

        mock_callback.assert_any_call("Воскресенье", "Привет")
        mock_callback.assert_any_call("работа", "машинлернер")
        self.assertEqual(mock_callback.call_count, 2)

    def test_process_json_no_tokens(self):
        json_str = (
            '{"Тут есть ключ": "Тут предложение", "Другой ключик": ' '"клавиатура"}'
        )
        required_keys = ["ключ", "ключик"]
        tokens = ["Отсутствие"]

        mock_callback = Mock()

        process_json(json_str, required_keys, tokens, mock_callback)

        mock_callback.assert_not_called()

    def test_process_json_uppercase(self):
        json_str = '{"имя": "Глеб", "работа": "машинлернер", "город": "Москва"}'
        required_keys = ["имя", "работа", "гОРОд"]
        tokens = ["глЕБ", "мАшИнЛеРнЕр", "Москва"]

        mock_callback = Mock()

        process_json(json_str, required_keys, tokens, mock_callback)

        mock_callback.assert_any_call("имя", "глЕБ")
        mock_callback.assert_any_call("работа", "мАшИнЛеРнЕр")
        self.assertEqual(mock_callback.call_count, 2)

    def test_process_json_key_no_match(self):
        json_str = '{"страна": "Россия"}'
        required_keys = ["имя", "работа"]
        tokens = ["Россия"]

        mock_callback = Mock()

        process_json(json_str, required_keys, tokens, mock_callback)

        mock_callback.assert_not_called()

    def test_process_json_punctuation(self):
        json_str = (
            '{"прозвище": "Глеб!!!", "должность_работа": "машинлернер, '
            "надеюсь в "
            "компании ($ВКонтакте!) начиная со следующего "
            'семестра..."}'
        )
        required_keys = ["прозвище", "должность_работа"]
        tokens = ["Глеб", "машинлернер", "семестра", "ВКонтакте"]

        mock_callback = Mock()

        process_json(json_str, required_keys, tokens, mock_callback)

        mock_callback.assert_any_call("прозвище", "Глеб")
        mock_callback.assert_any_call("должность_работа", "машинлернер")
        mock_callback.assert_any_call("должность_работа", "семестра")
        mock_callback.assert_any_call("должность_работа", "ВКонтакте")
        self.assertEqual(mock_callback.call_count, 4)

    def test_process_json_empty_keys(self):
        json_str = (
            '{"спам": "ээээээээээээм", "СПАМОВИЧ": "ну тут вообще '
            "ничего нет, тест нужен чтобы проверить корректность "
            'если вообще нет переданных ключей"}'
        )
        required_keys = []
        tokens = ["ну", "нет"]

        mock_callback = Mock()

        process_json(json_str, required_keys, tokens, mock_callback)

        mock_callback.assert_not_called()

    def test_process_json_empty_tokens(self):
        json_str = (
            '{"спам": "ээээээээээээм", "СПАМОВИЧ": "ну тут вообще '
            "ничего нет, тест нужен чтобы проверить корректность "
            'если вообще нет переданных токенов"}'
        )
        required_keys = ["спам", "СПАМОВИЧ"]
        tokens = []

        mock_callback = Mock()

        process_json(json_str, required_keys, tokens, mock_callback)

        mock_callback.assert_not_called()

    def test_process_json_multiple_tokens(self):
        json_str = (
            '{"отчество": "леонидович", "описание": "сегодня я '
            "полдня выводил формулки в bias-variance разложении, "
            "вроде всё в итоге понято и нормально, "
            "но после этого подумал - может стоило просто пойти "
            "фронтедером после девятого класса в школе? я не люблю "
            'городу Долгопрудный"}'
        )
        required_keys = ["описание"]
        tokens = ["ЛЕОНидовИЧ", "фронтедерОМ", "ДолгоПРУДНЫЙ", "формулки"]

        mock_callback = Mock()

        process_json(json_str, required_keys, tokens, mock_callback)

        mock_callback.assert_any_call("описание", "формулки")
        mock_callback.assert_any_call("описание", "фронтедерОМ")
        mock_callback.assert_any_call("описание", "ДолгоПРУДНЫЙ")
        self.assertEqual(mock_callback.call_count, 3)

    def test_process_json_key_is_sentence(self):
        json_str = (
            '{"в первой домашке Геннадий Кандауров предложил мне добавить '
            "тест на то, что ключ или токен уже не помню является целым "
            'предложением. вот тут я это и делаю!": "Сегодня я '
            'пошел в магазин, а потом встретил друга."}'
        )
        required_keys = [
            "в первой домашке Геннадий Кандауров предложил мне "
            "добавить тест на то, что ключ или токен уже не "
            "помню является целым предложением. вот тут я это и "
            "делаю!"
        ]
        tokens = ["пошел в магазин"]

        mock_callback = Mock()

        process_json(json_str, required_keys, tokens, mock_callback)

        mock_callback.assert_any_call(
            "в первой домашке Геннадий Кандауров "
            "предложил мне добавить тест на то, "
            "что ключ или токен уже не помню "
            "является целым предложением. вот тут я это и делаю!",
            "пошел в магазин",
        )
        self.assertEqual(mock_callback.call_count, 1)

    def test_process_json_token_is_sentence(self):
        json_str = (
            '{"я устал от долгих легенд в тестах.": "Геннадий, если вы это '
            'читаете - хорошего вам настроения!!!"}'
        )
        required_keys = ["я устал от долгих легенд в тестах."]
        tokens = ["Геннадий, если вы это читаете - хорошего вам настроения!!!"]

        mock_callback = Mock()

        process_json(json_str, required_keys, tokens, mock_callback)

        mock_callback.assert_any_call(
            "я устал от долгих легенд в тестах.",
            "Геннадий, если вы это " "читаете - хорошего вам настроения!!!",
        )
        self.assertEqual(mock_callback.call_count, 1)
