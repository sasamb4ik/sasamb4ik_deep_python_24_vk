import unittest
from custom_list import CustomList


class TestCustomList(unittest.TestCase):

    def setUp(self):
        '''
        Храним списки для тестов операторов сравнения
        '''
        self.cl1 = CustomList(1, 2, 3)
        self.cl2 = CustomList(3, 2, 1)
        self.cl3 = CustomList(4, 5)
        self.cl4 = CustomList()
        self.cl5 = CustomList([-item for item in range(10)])
        self.cl6 = CustomList(
            [(lambda x: x * -1 if x % 2 == 0 else x)(x) for x in range(10)]
            )

    def test_inheritance(self):
        self.assertTrue(issubclass(CustomList, list))

        custom_list = CustomList()

        self.assertIsInstance(custom_list, list)

    def test_init(self):
        custom_from_int = CustomList(1, 2, 3, 4)
        custom_from_list = CustomList([5, 6, 7, 8])
        custom_empty = CustomList()

        self.assertIsInstance(custom_from_int, CustomList)
        self.assertEqual(custom_from_int, CustomList(1, 2, 3, 4))

        self.assertIsInstance(custom_from_list, CustomList)
        self.assertEqual(custom_from_list, CustomList([5, 6, 7, 8]))

        self.assertIsInstance(custom_empty, CustomList)
        self.assertEqual(custom_empty, CustomList())

        invalid_inputs = [
            "привет",
            (2, 3),
            {2: 3, 4: 5},
            {1, 2, 3, 4}
        ]

        for invalid_input in invalid_inputs:
            with self.assertRaises(TypeError) as context:
                CustomList(invalid_input)
            self.assertEqual(
                str(context.exception),
                "CustomList можно создавать только из целых "
                "чисел и списков целых чисел."
            )

    def test_neg(self):
        self.assertEqual(
            CustomList(1, 2, 3).__neg__(),
            CustomList(-1, -2, -3)
        )

        self.assertEqual(
            CustomList([1, 2, 3]).__neg__(),
            CustomList(-1, -2, -3)
        )

        self.assertEqual(
            CustomList(1, 2, -3, -4, 0).__neg__(),
            CustomList(-1, -2, 3, 4, 0)
        )

        self.assertEqual(
            CustomList([-1, -2, -3, -4, 0]).__neg__(),
            CustomList(1, 2, 3, 4, 0)
        )

    def test_equality(self):
        self.assertEqual(self.cl1, self.cl2)

        self.assertEqual(self.cl6, CustomList(5))

        self.assertNotEqual(self.cl1, self.cl3)

        self.assertNotEqual(self.cl3, self.cl4)

        self.assertNotEqual(self.cl5, self.cl6)

        with self.assertRaises(TypeError) as context:
            _ = self.cl1 == [6]
        self.assertEqual(
            str(context.exception),
            "Сравнение можно производить только с объектами класса CustomList."
        )

        with self.assertRaises(TypeError) as context:
            _ = self.cl1 == "some string"
        self.assertEqual(
            str(context.exception),
            "Сравнение можно производить только с объектами класса CustomList."
        )

    def test_inequality(self):
        self.assertNotEqual(self.cl1, self.cl3)

        self.assertNotEqual(self.cl3, self.cl4)

        self.assertNotEqual(self.cl5, self.cl6)

        self.assertNotEqual(self.cl6, CustomList(6))

        with self.assertRaises(TypeError) as context:
            _ = self.cl1 != [6]
        self.assertEqual(
            str(context.exception),
            "Сравнение можно производить только с объектами класса CustomList."
        )

        with self.assertRaises(TypeError) as context:
            _ = self.cl1 != "some string"
        self.assertEqual(
            str(context.exception),
            "Сравнение можно производить только с объектами класса CustomList."
        )

    def test_less_and_great(self):
        self.assertFalse(self.cl1 < self.cl2)

        self.assertTrue(self.cl3 > self.cl4)

        self.assertTrue(self.cl5 < self.cl6)

        self.assertTrue(CustomList([5, 5, 5, 10]) <= CustomList([5, 5, 5, 10]))

        self.assertTrue(CustomList([5, 5, 5, 10]) >= CustomList([5, 5, 5, 10]))

        self.assertFalse(CustomList([5, 5, 5, 10]) > CustomList([5, 5, 5, 10]))

        with self.assertRaises(TypeError) as context:
            _ = self.cl1 < [6]
        self.assertEqual(
            str(context.exception),
            "Сравнение можно производить только с объектами класса CustomList."
        )

        with self.assertRaises(TypeError) as context:
            _ = self.cl1 > 5
        self.assertEqual(
            str(context.exception),
            "Сравнение можно производить только с объектами класса CustomList."
        )

    def test_arithmetic_operations_and_unchanged(self):

        self.assertEqual(self.cl1 + self.cl2, CustomList(4, 4, 4))
        self.assertEqual(self.cl1, CustomList(1, 2, 3))
        self.assertEqual(self.cl2, CustomList(3, 2, 1))

        self.assertEqual(self.cl1 - self.cl2, CustomList(-2, 0, 2))
        self.assertEqual(self.cl1, CustomList(1, 2, 3))
        self.assertEqual(self.cl2, CustomList(3, 2, 1))

        self.assertEqual(self.cl1 + [100, 200], CustomList(101, 202, 3))
        self.assertEqual(self.cl1, CustomList(1, 2, 3))

        self.assertEqual(self.cl1 - [100], CustomList(-99, 2, 3))
        self.assertEqual(self.cl1, CustomList(1, 2, 3))

        self.assertEqual([100, 200, 300] + self.cl2, CustomList(103, 202, 301))
        self.assertEqual(self.cl2, CustomList(3, 2, 1))

        self.assertEqual([100, 200, 300] - self.cl2, CustomList(97, 198, 299))
        self.assertEqual(self.cl2, CustomList(3, 2, 1))

        self.assertEqual([] + self.cl2, CustomList(3, 2, 1))
        self.assertEqual(self.cl2, CustomList(3, 2, 1))

        self.assertEqual([] - self.cl2, CustomList(-3, -2, -1))
        self.assertEqual(self.cl2, CustomList(3, 2, 1))

        self.assertEqual(self.cl2 - [], CustomList(3, 2, 1))
        self.assertEqual(self.cl2, CustomList(3, 2, 1))

        self.assertEqual(CustomList() + CustomList(), CustomList())

        self.assertEqual(self.cl5 + 100, CustomList([100, 99, 98, 97, 96, 95,
                                                     94, 93, 92, 91]))
        self.assertEqual(self.cl5, CustomList([0, -1, -2, -3, -4,
                                               -5, -6, -7,-8, -9]))


        self.assertEqual(self.cl1 - 100, CustomList(-99, -98, -97))
        self.assertEqual(self.cl1, CustomList(1, 2, 3))

        self.assertEqual(100 - self.cl1, CustomList(99, 98, 97))
        self.assertEqual(self.cl1, CustomList(1, 2, 3))

    def test_str_method(self):

        cl = CustomList([1, 2, 3, 4, 5])
        expected_str = "Элементы CustomList: (1, 2, 3, 4, 5)\nСумма элементов: 15"
        self.assertEqual(str(cl), expected_str)

        empty_cl = CustomList()
        expected_empty_str = "Элементы CustomList: ()\nСумма элементов: 0"
        self.assertEqual(str(empty_cl), expected_empty_str)

        cl_neg = CustomList([-1, -2, -3])
        expected_neg_str = "Элементы CustomList: (-1, -2, -3)\nСумма элементов: -6"
        self.assertEqual(str(cl_neg), expected_neg_str)

        cl_mixed = CustomList(-1, 0, 1)
        expected_mixed_str = "Элементы CustomList: (-1, 0, 1)\nСумма элементов: 0"
        self.assertEqual(str(cl_mixed), expected_mixed_str)















