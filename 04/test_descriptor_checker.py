import unittest
from descriptor_checker import Data


class TestDescriptors(unittest.TestCase):

    def setUp(self):
        self.data = Data(num=1, name="Test", price=100)

    def test_init(self):
        self.assertEqual(self.data.num, 1)
        self.assertEqual(self.data.name, "Test")
        self.assertEqual(self.data.price, 100)

    def test_set_correct_types(self):
        self.data.num = 10
        self.data.name = "Новое значение"
        self.data.price = 200
        self.assertEqual(self.data.num, 10)
        self.assertEqual(self.data.name, "Новое значение")
        self.assertEqual(self.data.price, 200)

    def test_set_incorrect_type_num(self):
        with self.assertRaises(TypeError):
            self.data.num = "это строка а не интеджер"

    def test_set_incorrect_name(self):
        with self.assertRaises(TypeError):
            self.data.name = 123

    def test_set_incorrect_price(self):
        with self.assertRaises(TypeError):
            self.data.price = "это не интеджер"

    def test_set_negative_price(self):
        with self.assertRaises(ValueError):
            self.data.price = -50

    def test_delete_attribute(self):
        with self.assertRaises(AttributeError):
            del self.data.num
        with self.assertRaises(AttributeError):
            del self.data.name
        with self.assertRaises(AttributeError):
            del self.data.price

    def test_descriptor_multiplicity(self):
        data1 = Data(num=2, name="Data1", price=150)
        data2 = Data(num=3, name="Data2", price=250)
        self.assertEqual(data1.num, 2)
        self.assertEqual(data1.name, "Data1")
        self.assertEqual(data1.price, 150)

        self.assertEqual(data2.num, 3)
        self.assertEqual(data2.name, "Data2")
        self.assertEqual(data2.price, 250)

        data1.num = 4
        self.assertEqual(data1.num, 4)
        self.assertEqual(data2.num, 3)

    def test_descriptor_positive_integer(self):
        self.data.price = 500
        self.assertEqual(self.data.price, 500)
        with self.assertRaises(ValueError):
            self.data.price = 0
        with self.assertRaises(ValueError):
            self.data.price = -10
