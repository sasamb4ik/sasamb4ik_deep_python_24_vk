import string
from io import TextIOBase


def _remove_punctuation(given_string: str) -> str:
    table = str.maketrans(dict.fromkeys(string.punctuation))
    return given_string.translate(table)


def _process_words(file_or_filename, stops, searching):
    for line in file_or_filename:
        stripped_line = _remove_punctuation(line).strip().lower()

        if stripped_line in stops:
            continue

        if stripped_line in searching:
            yield line.strip()
            continue

        current_words = set(stripped_line.split())

        if current_words & stops:
            continue

        if any(word in current_words for word in searching):
            yield line.strip()


def search_file_generator(file_or_name, search_words: list[str], stop_words: list[str]):
    stops = set(word.lower() for word in stop_words)
    searching = set(word.lower() for word in search_words)

    if isinstance(file_or_name, str):
        with open(file_or_name, "r", encoding="utf-8") as file:
            return _process_words(file, stops, searching)

    elif isinstance(file_or_name, TextIOBase):
        return _process_words(file_or_name, stops, searching)

    else:
        raise ValueError(
            "Некорректный ввод: file_or_name может быть либо именем файла, "
            "либо файловым объектом."
        )
