import unittest
from custom_list import CustomList


class TestCustomList(unittest.TestCase):

    def test_inheritance(self):
        self.assertTrue(issubclass(CustomList, list))

        custom_list = CustomList()

        self.assertIsInstance(custom_list, list)

    def test_init(self):
        """
        Добавил проверку создания из контейнеров и от итератора
        """
        custom_from_int = CustomList(1, 2, 3, 4)
        custom_from_list = CustomList([5, 6, 7, 8])
        custom_from_tuple = CustomList((9, 10, 11))
        custom_from_set = CustomList({12, 13, 14})
        custom_empty = CustomList()

        custom_from_iterator = CustomList(iter([15, 16, 17]))
        custom_from_floats = CustomList(3.14, 2.71)

        self.assertIsInstance(custom_from_int, CustomList)
        self.assertEqual(custom_from_int, CustomList(1, 2, 3, 4))

        self.assertIsInstance(custom_from_list, CustomList)
        self.assertEqual(custom_from_list, CustomList([5, 6, 7, 8]))

        self.assertIsInstance(custom_from_tuple, CustomList)
        self.assertEqual(custom_from_tuple, CustomList((9, 10, 11)))

        self.assertIsInstance(custom_from_set, CustomList)
        self.assertTrue(set(custom_from_set) == {12, 13, 14})

        self.assertIsInstance(custom_empty, CustomList)
        self.assertEqual(custom_empty, CustomList())

        self.assertIsInstance(custom_from_iterator, CustomList)
        self.assertEqual(custom_from_iterator, CustomList(15, 16, 17))

        self.assertIsInstance(custom_from_floats, CustomList)
        self.assertEqual(custom_from_floats, CustomList(3.14, 2.71))

    def test_neg(self):
        self.assertEqual(-CustomList(1, 2, 3), CustomList(-1, -2, -3))
        self.assertEqual(-CustomList([1, 2, 3]), CustomList(-1, -2, -3))
        self.assertEqual(
            -CustomList(1, 2, -3, -4, 0), CustomList(-1, -2, 3, 4, 0)
        )
        self.assertEqual(
            -CustomList([-1, -2, -3, -4, 0]), CustomList(1, 2, 3, 4, 0)
        )

    def test_equality(self):
        cl1 = CustomList(1, 2, 3)
        cl2 = CustomList(3, 2, 1)
        cl3 = CustomList(4, 5)
        cl4 = CustomList()
        cl5 = CustomList([-item for item in range(10)])
        cl6 = CustomList([-x if x % 2 == 0 else x for x in range(10)])

        self.assertEqual(cl1, cl2)
        self.assertEqual(cl6, CustomList(5))
        self.assertNotEqual(cl1, cl3)
        self.assertNotEqual(cl3, cl4)
        self.assertNotEqual(cl5, cl6)

        with self.assertRaises(TypeError) as context:
            _ = cl1 == [6]
        self.assertEqual(
            str(context.exception),
            "Сравнение можно производить только с объектами класса CustomList.",
        )

        with self.assertRaises(TypeError) as context:
            _ = cl1 == "some string"
        self.assertEqual(
            str(context.exception),
            "Сравнение можно производить только с объектами класса CustomList.",
        )

    def test_inequality(self):
        cl1 = CustomList(1, 2, 3)
        cl3 = CustomList(4, 5)
        cl4 = CustomList()
        cl5 = CustomList([-item for item in range(10)])
        cl6 = CustomList([-x if x % 2 == 0 else x for x in range(10)])

        self.assertNotEqual(cl1, cl3)
        self.assertNotEqual(cl3, cl4)
        self.assertNotEqual(cl5, cl6)
        self.assertNotEqual(cl6, CustomList(6))

        with self.assertRaises(TypeError) as context:
            _ = cl1 != [6]
        self.assertEqual(
            str(context.exception),
            "Сравнение можно производить только с объектами класса CustomList.",
        )

        with self.assertRaises(TypeError) as context:
            _ = cl1 != "some string"
        self.assertEqual(
            str(context.exception),
            "Сравнение можно производить только с объектами класса CustomList.",
        )

    def test_less_and_great(self):
        cl1 = CustomList(1, 2, 3)
        cl2 = CustomList(3, 2, 1)
        cl3 = CustomList(4, 5)
        cl4 = CustomList()
        cl5 = CustomList([-item for item in range(10)])
        cl6 = CustomList([-x if x % 2 == 0 else x for x in range(10)])

        self.assertFalse(cl1 < cl2)
        self.assertTrue(cl3 > cl4)
        self.assertTrue(cl5 < cl6)
        self.assertTrue(CustomList([5, 5, 5, 10]) <= CustomList([5, 5, 5, 10]))
        self.assertTrue(CustomList([5, 5, 5, 10]) >= CustomList([5, 5, 5, 10]))
        self.assertFalse(CustomList([5, 5, 5, 10]) > CustomList([5, 5, 5, 10]))

        with self.assertRaises(TypeError) as context:
            _ = cl1 < [6]
        self.assertEqual(
            str(context.exception),
            "Сравнение можно производить только с объектами класса CustomList.",
        )

        with self.assertRaises(TypeError) as context:
            _ = cl1 > 5
        self.assertEqual(
            str(context.exception),
            "Сравнение можно производить только с объектами класса CustomList.",
        )

    def assert_custom_list_equal(self, list1, list2):
        """
        Функция поэлементно проверяет равенство двух CustomList
        """
        self.assertEqual(len(list1), len(list2), "У списков разная длина")
        self.assertListEqual(
            list(list1), list(list2), "Списки не совпадают поэлементно"
        )

    def test_arithmetic_operations_and_unchanged(self):
        """
        Тесты на корректность операций сложения и вычитания, с проверкой
        поэлементного соответствия результата.
        В конце этой функции я добавил тесты, показывающие результат
        исправлений, который не отловился бы старым __eq__
        """
        cl1 = CustomList(1, 2, 3)
        cl2 = CustomList(3, 2, 1)
        cl5 = CustomList([-item for item in range(10)])

        self.assert_custom_list_equal(cl1 + cl2, CustomList(4, 4, 4))
        self.assert_custom_list_equal(cl1, CustomList(1, 2, 3))
        self.assert_custom_list_equal(cl2, CustomList(3, 2, 1))

        self.assert_custom_list_equal(cl1 - cl2, CustomList(-2, 0, 2))
        self.assert_custom_list_equal(cl1, CustomList(1, 2, 3))
        self.assert_custom_list_equal(cl2, CustomList(3, 2, 1))

        self.assert_custom_list_equal(cl1 + [100, 200], CustomList(101, 202, 3))
        self.assert_custom_list_equal(cl1, CustomList(1, 2, 3))

        self.assert_custom_list_equal(cl1 - [100], CustomList(-99, 2, 3))
        self.assert_custom_list_equal(cl1, CustomList(1, 2, 3))

        self.assert_custom_list_equal(
            [100, 200, 300] + cl2, CustomList(103, 202, 301)
        )
        self.assert_custom_list_equal(cl2, CustomList(3, 2, 1))

        self.assert_custom_list_equal(
            [100, 200, 300] - cl2, CustomList(97, 198, 299)
        )
        self.assert_custom_list_equal(cl2, CustomList(3, 2, 1))

        self.assert_custom_list_equal([] + cl2, CustomList(3, 2, 1))
        self.assert_custom_list_equal(cl2, CustomList(3, 2, 1))

        self.assert_custom_list_equal([] - cl2, CustomList(-3, -2, -1))
        self.assert_custom_list_equal(cl2, CustomList(3, 2, 1))

        self.assert_custom_list_equal(cl2 - [], CustomList(3, 2, 1))
        self.assert_custom_list_equal(cl2, CustomList(3, 2, 1))

        self.assert_custom_list_equal(CustomList() + CustomList(), CustomList())

        self.assert_custom_list_equal(
            cl5 + 100, CustomList([100, 99, 98, 97, 96, 95, 94, 93, 92, 91])
        )
        self.assert_custom_list_equal(
            cl5, CustomList([0, -1, -2, -3, -4, -5, -6, -7, -8, -9])
        )

        self.assert_custom_list_equal(cl1 - 100, CustomList(-99, -98, -97))
        self.assert_custom_list_equal(cl1, CustomList(1, 2, 3))

        self.assert_custom_list_equal(100 - cl1, CustomList(99, 98, 97))
        self.assert_custom_list_equal(cl1, CustomList(1, 2, 3))

        # проверка когда сумма/разность совпадают, но поэлементно разные
        sum_equal_diff_elements_add = CustomList(5, 3, 4)
        sum_equal_diff_elements_sub = CustomList(-1, -1, 2)

        self.assert_custom_list_equal(cl1 + cl2, CustomList(4, 4, 4))
        self.assertNotEqual(
            list(cl1 + cl2),
            list(sum_equal_diff_elements_add),
            "Списки совпадают по сумме, но не по элементам",
        )

        self.assert_custom_list_equal(cl1 - cl2, CustomList(-2, 0, 2))
        self.assertNotEqual(
            list(cl1 - cl2),
            list(sum_equal_diff_elements_sub),
            "Списки совпадают по сумме, но не по элементам",
        )

    def test_str_method(self):
        cl = CustomList([1, 2, 3, 4, 5])
        expected_str = (
            "Элементы CustomList: (1, 2, 3, 4, 5)\nСумма элементов: 15"
        )
        self.assertEqual(str(cl), expected_str)

        empty_cl = CustomList()
        expected_empty_str = "Элементы CustomList: ()\nСумма элементов: 0"
        self.assertEqual(str(empty_cl), expected_empty_str)

        cl_neg = CustomList([-1, -2, -3])
        expected_neg_str = (
            "Элементы CustomList: (-1, -2, -3)\nСумма элементов: -6"
        )
        self.assertEqual(str(cl_neg), expected_neg_str)

        cl_mixed = CustomList(-1, 0, 1)
        expected_mixed_str = (
            "Элементы CustomList: (-1, 0, 1)\nСумма элементов: 0"
        )
        self.assertEqual(str(cl_mixed), expected_mixed_str)
