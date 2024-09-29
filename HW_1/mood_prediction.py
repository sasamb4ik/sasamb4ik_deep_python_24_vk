class SomeModel:

    @staticmethod
    def count_vowels(message: str) -> int:
        """
        message: str -> Поданная на вход строка
        Функция возвращает кол-во гласных в строке message
        """
        vowels_set = {"a", "e", "i", "o", "u"}
        return sum(1 for char in message if char.lower() in vowels_set)

    def predict(self, message: str) -> float:
        """
        message: Cтрока, состоящая только из букв Unicode формата
        Ф-я возвращает отношение гласных букв в строке message к длине message
        Букву Y за гласную считать не будем (это как Й в русском языке,
        она не явл-ся гласной).
        """

        if not message:
            raise ValueError("Вы передали пустую строку.")

        if not all(char.isalpha() for char in message):
            raise ValueError(
                "Неверный входной формат строки. "
                "Строка должна состоять только из букв Unicode формата."
            )

        return round(self.count_vowels(message) / len(message), 3)


def predict_message_mood(
    message: str,
    bad_thresholds: float = 0.3,
    good_thresholds: float = 0.8,
) -> str:
    model = SomeModel()
    value = model.predict(message)

    if value < bad_thresholds:
        return "неуд"
    if value > good_thresholds:
        return "отл"
    return "норм"
