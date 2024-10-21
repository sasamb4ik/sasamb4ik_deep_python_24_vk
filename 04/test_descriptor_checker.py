import unittest
from descriptor_checker import Data


class TestDescriptors(unittest.TestCase):

    def setUp(self):
        self.data = Data(num=1, name="Test", price=100)

    def test_init(self):
        self.assertEqual(self.data.num, 1, "Инициализация 'num' некорректна")
        self.assertEqual(
            self.data.name, "Test", "Инициализация 'name' некорректна"
        )
        self.assertEqual(
            self.data.price, 100, "Инициализация 'price' некорректна"
        )

    def test_set_correct_types(self):
        try:
            self.data.num = 10
            self.assertEqual(
                self.data.num, 10, "'num' не был присвоен корректно"
            )
        except TypeError:
            self.fail("'num' вызвал TypeError при присвоении корректного типа")

        try:
            self.data.name = "Новое значение"
            self.assertEqual(
                self.data.name,
                "Новое значение",
                "'name' не был присвоен корректно",
            )
        except TypeError:
            self.fail("'name' вызвал TypeError при присвоении корректного типа")

        try:
            self.data.price = 200
            self.assertEqual(
                self.data.price, 200, "'price' не был присвоен корректно"
            )
        except (TypeError, ValueError):
            self.fail(
                "'price' вызвал исключение при присвоении корректного типа"
            )

    def test_set_incorrect_type_num(self):
        """
        Тут я сохраняю старое значение и далее проверяю, что оно не изменилось
        """
        current_value = self.data.num
        with self.assertRaises(
            TypeError,
            msg="'num' не вызвал TypeError при присвоении некорректного типа",
        ):
            self.data.num = "это строка а не интеджер"
        self.assertEqual(
            self.data.num,
            current_value,
            "Изменение на невалидное значение изменило 'num'",
        )

    def test_set_incorrect_name(self):
        """
        Тут я сохраняю старое значение и далее проверяю, что оно не изменилось
        """
        current_value = self.data.name
        with self.assertRaises(
            TypeError,
            msg="'name' не вызвал TypeError при присвоении некорректного типа",
        ):
            self.data.name = 123
        self.assertEqual(
            self.data.name,
            current_value,
            "Изменение на невалидное значение изменило 'name'",
        )

    def test_set_incorrect_price(self):
        current_value = self.data.price
        with self.assertRaises(
            TypeError,
            msg="'price' не вызвал TypeError при присвоении некорректного типа",
        ):
            self.data.price = "это не интеджер"
        self.assertEqual(
            self.data.price,
            current_value,
            "Изменение на невалидное значение изменило 'price'",
        )

    def test_set_negative_price(self):
        current_value = self.data.price
        with self.assertRaises(
            ValueError,
            msg="'price' не вызвал ValueError при"
                "присвоении отрицательного значения",
        ):
            self.data.price = -50
        self.assertEqual(
            self.data.price,
            current_value,
            "Присвоение отрицательного значения изменило 'price'",
        )

    def test_delete_attribute(self):
        with self.assertRaises(
            AttributeError, msg="Удаление 'num' не вызвало AttributeError"
        ):
            del self.data.num
        with self.assertRaises(
            AttributeError, msg="Удаление 'name' не вызвало AttributeError"
        ):
            del self.data.name
        with self.assertRaises(
            AttributeError, msg="Удаление 'price' не вызвало AttributeError"
        ):
            del self.data.price

    def test_descriptor_multiplicity(self):
        data1 = Data(num=2, name="Data1", price=150)
        data2 = Data(num=3, name="Data2", price=250)

        self.assertEqual(
            data1.num, 2, "'num' в data1 был инициализирован некорректно"
        )
        self.assertEqual(
            data1.name,
            "Data1",
            "'name' в data1 был инициализирован некорректно",
        )
        self.assertEqual(
            data1.price, 150, "'price' в data1 был инициализирован некорректно"
        )

        self.assertEqual(
            data2.num, 3, "'num' в data2 был инициализирован некорректно"
        )
        self.assertEqual(
            data2.name,
            "Data2",
            "'name' в data2 был инициализирован некорректно",
        )
        self.assertEqual(
            data2.price, 250, "'price' в data2 был инициализирован некорректно"
        )

        data1.num = 4
        data1.name = "UpdatedData1"
        data1.price = 175

        self.assertEqual(data1.num, 4, "'num' в data1 не был изменен корректно")
        self.assertEqual(
            data1.name,
            "UpdatedData1",
            "'name' в data1 не был изменен корректно",
        )
        self.assertEqual(
            data1.price, 175, "'price' в data1 не был изменен корректно"
        )

        self.assertEqual(data2.num, 3, "'num' в data2 изменился некорректно")
        self.assertEqual(
            data2.name, "Data2", "'name' в data2 изменился некорректно"
        )
        self.assertEqual(
            data2.price, 250, "'price' в data2 изменился некорректно"
        )

    def test_descriptor_positive_integer(self):
        self.data.price = 500
        self.assertEqual(
            self.data.price, 500, "'price' не был присвоен корректно"
        )
        with self.assertRaises(
            ValueError,
            msg="'price' не вызвал ValueError при присвоении значения 0",
        ):
            self.data.price = 0
        with self.assertRaises(
            ValueError,
            msg="'price' не вызвал ValueError при"
                "присвоении отрицательного значения",
        ):
            self.data.price = -10
