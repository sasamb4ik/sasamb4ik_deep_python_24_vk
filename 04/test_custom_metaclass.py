import unittest
from custom_metaclass import CustomMeta


class TestCustomMeta(unittest.TestCase):

    def setUp(self):
        class CustomClass(metaclass=CustomMeta):
            x = 50

            def __init__(self, val=99):
                self.val = val

            def line(self):
                return 100

            def __str__(self):
                return "Custom_by_metaclass"

        self.cls = CustomClass
        self.instance = CustomClass()

    def test_class_attribute_access(self):
        self.assertEqual(self.cls.custom_x, 50)

        with self.assertRaises(AttributeError):
            _ = self.cls.x

    def test_instance_attribute_access(self):
        self.assertEqual(self.instance.custom_x, 50)
        self.assertEqual(self.instance.custom_val, 99)
        self.assertEqual(self.instance.custom_line(), 100)
        self.assertEqual(str(self.instance), "Custom_by_metaclass")

        with self.assertRaises(AttributeError):
            _ = self.instance.x
        with self.assertRaises(AttributeError):
            _ = self.instance.val
        with self.assertRaises(AttributeError):
            _ = self.instance.line()
        with self.assertRaises(AttributeError):
            _ = self.instance.yyy

    def test_dynamic_creation(self):
        self.instance.dynamic = "added later"

        self.instance.some_attribute = "some value"

        setattr(self.instance, "new_method", lambda self: "new method")

        self.assertEqual(self.instance.custom_dynamic, "added later")
        self.assertEqual(self.instance.custom_some_attribute, "some value")
        self.assertEqual(self.instance.custom_new_method(self.instance), "new method")

        with self.assertRaises(AttributeError):
            _ = self.instance.dynamic
        with self.assertRaises(AttributeError):
            _ = self.instance.some_attribute
        with self.assertRaises(AttributeError):
            _ = self.instance.new_method(self.instance)

    def test_inheritance(self):
        class SubCustomClass(self.cls):
            y = 200

            def method_sub(self):
                return 300

            def __repr__(self):
                return "SubCustomClass"

        self.assertEqual(SubCustomClass.custom_x, 50)
        self.assertEqual(SubCustomClass.custom_y, 200)
        self.assertEqual(SubCustomClass.custom_method_sub(self.instance), 300)

        instance_sub = SubCustomClass()
        self.assertEqual(repr(instance_sub), "SubCustomClass")

        with self.assertRaises(AttributeError):
            _ = SubCustomClass.x
        with self.assertRaises(AttributeError):
            _ = SubCustomClass.y
        with self.assertRaises(AttributeError):
            _ = SubCustomClass.method_sub(instance_sub)

    def test_attribute_deletion(self):
        self.assertEqual(self.instance.custom_val, 99)

        del self.instance.custom_val

        with self.assertRaises(AttributeError):
            _ = self.instance.custom_val

        with self.assertRaises(AttributeError):
            del self.instance.val

    def test_setting_magic_attribute(self):
        self.instance.__custom_magic__ = "magic"
        self.assertEqual(self.instance.__custom_magic__, "magic")
        with self.assertRaises(AttributeError):
            _ = self.instance.custom__custom_magic__
