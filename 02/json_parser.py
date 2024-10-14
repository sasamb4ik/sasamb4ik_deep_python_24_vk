import json
from typing import Callable
import string


def remove_punctuation(given_string: str) -> str:
    table = str.maketrans(dict.fromkeys(string.punctuation))
    return given_string.translate(table)


def process_json(
    json_str: str,
    required_keys: list[str] | None = None,
    tokens: list[str] | None = None,
    callback: Callable[[str, str], None] | None = None,
) -> None:
    """
    Функция подразумевает следующую логику: будем очищать от пунктуации и
    ключ в json'е, и элементы required_keys, токены тоже будем очищать от
    пунктуации. Функция-обработчик будет вызываться от очищенных от
    пунктуации ключа и токена.
    """

    '''
    Замечание: нужно обрабатывать случаи, когда required_keys или tokens
    или callback равны None
    Правки: по решению автора (меня), функция при таких случаяз просто будет 
    терминироваться
    '''

    if required_keys or tokens or callback is None:
        raise ValueError('required_keys, tokens или callback равны None. '
                         'Проверьте ввод!')

    json_dict = json.loads(json_str)

    # Удаляем пунктуацию из ключей для сравнения
    set_req_filtered_keys = set(remove_punctuation(item)
                                for item in required_keys)

    for json_key, json_value in json_dict.items():
        valid_key = remove_punctuation(json_key)
        if valid_key in set_req_filtered_keys:
            # Очищаем значение от пунктуации и приводим к нижнему регистру
            cleaned_value = remove_punctuation(json_value).strip().lower()

            # Поиск токенов целиком в строке значения
            for token in tokens:
                cleaned_token = remove_punctuation(token.lower())
                if cleaned_token in cleaned_value:
                    # Вызываем коллбек, если токен найден
                    callback(json_key, token)
