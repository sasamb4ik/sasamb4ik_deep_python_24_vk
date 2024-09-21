import string


def remove_punctuation(given_string: str) -> str:
    table = str.maketrans(
        dict.fromkeys(string.punctuation)
    )
    return given_string.translate(table)


def search_file_generator(
        file_name, search_words: list[str],
        stop_words: list[str]
):
    stops = set(word.lower() for word in stop_words)
    searching = set(word.lower() for word in search_words)

    with open(file_name, 'r', encoding='utf-8') as file:
        for line in file:
            current_words = set(
                remove_punctuation(line).strip().lower().split()
                )
            if current_words & stops: continue
            if any(word in current_words for word in searching):
                yield line.strip()
