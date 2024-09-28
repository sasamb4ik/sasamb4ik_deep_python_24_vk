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
    Предполагаем, что в required_keys и tokens находятся корректные слова (
    без пунктуации и лишних символов). Также предполагаем, что если например
    в required_keys лежит слово "key", и в json'е ключом является "key!",
    то мы хотим учитывать этот ключ, то есть реализация не зависит от
    пунктуации (аналогично и для tokens).
    """

    json_dict = json.loads(json_str)
    json_keys = json_dict.keys()
    set_required_keys = set(required_keys)
    for json_key in json_keys:
        valid_key = remove_punctuation(json_key)
        if valid_key in set_required_keys:
            set_json_value_words = set(
                remove_punctuation(json_dict[json_key]).strip().lower().split()
            )

            for token in tokens:
                if token.lower() in set_json_value_words:
                    callback(json_key, token)
