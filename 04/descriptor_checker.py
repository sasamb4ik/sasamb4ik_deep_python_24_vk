class BaseDescriptor:

    def __init__(self):
        self.private_name = None

    def __set_name__(self, owner, name):
        self.private_name = f"_{name}"

    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return getattr(instance, self.private_name, None)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.private_name, value)

    def __delete__(self, instance):
        raise AttributeError("Удаление атрибута запрещено.")

    def validate(self, value):
        raise NotImplementedError(
            "Метод validate должен быть реализован в наследующем классе."
        )


class Integer(BaseDescriptor):
    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Ожидается int, получено {type(value).__name__}.")


class String(BaseDescriptor):
    def validate(self, value):
        if not isinstance(value, str):
            raise TypeError(f"Ожидается str, получено {type(value).__name__}.")


class PositiveInteger(BaseDescriptor):
    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Ожидается int, получено {type(value).__name__}.")
        if value <= 0:
            raise ValueError("Значение должно быть положительным")


class Data:

    num = Integer()
    name = String()
    price = PositiveInteger()

    def __init__(self, num, name, price):
        self.num = num
        self.name = name
        self.price = price


a = bool(5 or 7 in (3, 6))
print(a)
