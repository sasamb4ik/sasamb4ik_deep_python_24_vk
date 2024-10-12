class CustomList(list):

    def __init__(self, *args):
        super().__init__()

        for arg in args:
            if isinstance(arg, list):
                self.extend(arg)
            elif isinstance(arg, int):
                self.append(arg)
            else:
                raise TypeError(
                    "CustomList можно создавать только из целых "
                    "чисел и списков целых чисел."
                )

    def __neg__(self):
        return CustomList([-item for item in self])

    def __add__(self, other):
        if isinstance(other, (CustomList, list)):
            max_len = max(len(self), len(other))
            result = CustomList(
                [
                    (self[i] if i < len(self) else 0)
                    + (other[i] if i < len(other) else 0)
                    for i in range(max_len)
                ]
            )
            return result
        if isinstance(other, int):
            return CustomList([x + other for x in self])
        raise TypeError(
            "CustomList поддерживает арифметические "
            "операции только с объектами класса, списками и целыми числами."
        )

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, int):
            return self.__add__(-other)
        if isinstance(other, (CustomList, list)):
            neg_other = CustomList([-item for item in other])
            return self.__add__(neg_other)
        raise TypeError(
            "CustomList поддерживает арифметические "
            "операции только с объектами класса, списками и целыми числами."
        )

    def __rsub__(self, other):
        if isinstance(other, (CustomList, list, int)):
            return -self.__sub__(other)
        raise TypeError(
            "CustomList поддерживает арифметические "
            "операции только с объектами класса, списками и целыми числами."
        )

    def __eq__(self, other):
        if isinstance(other, CustomList):
            return sum(self) == sum(other)
        raise TypeError(
            "Сравнение можно производить только с объектами класса CustomList."
        )

    def __ne__(self, other):
        return not self == other

    def __lt__(self, other):
        if isinstance(other, CustomList):
            return sum(self) < sum(other)
        raise TypeError(
            "Сравнение можно производить только с объектами класса CustomList."
        )

    def __ge__(self, other):
        return not self < other

    def __gt__(self, other):
        return not self == other and not self < other

    def __le__(self, other):
        return not self > other

    def __str__(self):
        elements_str = ", ".join(map(str, self))
        total_sum = sum(self)
        return (
            f"Элементы CustomList: ({elements_str})\n"
            f"Сумма элементов: {total_sum}"
        )
