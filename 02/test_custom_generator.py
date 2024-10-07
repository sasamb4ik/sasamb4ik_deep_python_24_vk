import unittest
import sys
from unittest.mock import Mock
from io import StringIO
from custom_generator import retry_deco


class TestParamDeco(unittest.TestCase):
    def test_default_deco(self):
        mock_function = Mock()
        mock_function.__name__ = "mock_function"

        mock_function.side_effect = [
            Exception("Error"),
            Exception("Error"),
            "Success",
        ]

        decorated_function = retry_deco(3)(mock_function)

        captured_output = StringIO()
        sys.stdout = captured_output

        result = decorated_function()

        sys.stdout = sys.__stdout__

        self.assertEqual(result, "Success")

        self.assertEqual(mock_function.call_count, 3)

        output = captured_output.getvalue()
        self.assertIn("attempt = 1, exception = Exception", output)
        self.assertIn("attempt = 2, exception = Exception", output)
        self.assertIn("attempt = 3, result = Success", output)

    def test_no_retry_on_exception(self):
        mock_function = Mock()
        mock_function.__name__ = "mock_function"

        mock_function.side_effect = ValueError("Expected error")

        decorated_function = retry_deco(3, exceptions=[ValueError])(
            mock_function
        )

        captured_output = StringIO()
        sys.stdout = captured_output

        with self.assertRaises(ValueError):
            decorated_function()

        sys.stdout = sys.__stdout__

        self.assertEqual(mock_function.call_count, 1)
        output = captured_output.getvalue()
        self.assertIn("attempt = 1, exception = ValueError", output)
        self.assertNotIn("attempt = 2", output)

    def test_one_retry(self):
        mock_function = Mock()
        mock_function.__name__ = "mock_function"
        mock_function.side_effect = [Exception("Error"), "Success"]

        decorated_function = retry_deco(1)(mock_function)

        with self.assertRaises(Exception) as _:
            decorated_function()

        self.assertEqual(mock_function.call_count, 1)

    def test_function_amount_of_reties_one(self):
        @retry_deco(3)
        def successful_function():
            return "Success"

        result = successful_function()
        self.assertEqual(result, "Success")

    def test_amount_of_retries_zero(self):
        with self.assertRaises(ValueError):
            retry_deco(0)

    def test_exceptions_empty_list(self):
        mock_function = Mock()
        mock_function.__name__ = "mock_function"
        mock_function.side_effect = [Exception("Error"), "Success"]

        decorated_function = retry_deco(3, exceptions=[])(mock_function)

        result = decorated_function()

        self.assertEqual(result, "Success")
        self.assertEqual(mock_function.call_count, 2)

    def test_multiple_exceptions_in_exceptions(self):
        mock_function = Mock()
        mock_function.__name__ = "mock_function"
        mock_function.side_effect = TypeError("Type error")

        decorated_function = retry_deco(3, exceptions=(ValueError, TypeError))(
            mock_function
        )

        with self.assertRaises(TypeError):
            decorated_function()

        self.assertEqual(mock_function.call_count, 1)

    def test_function_always_succeeds(self):
        mock_function = Mock(return_value="Success")
        mock_function.__name__ = "mock_function"

        decorated_function = retry_deco(3)(mock_function)

        result = decorated_function()

        self.assertEqual(result, "Success")
        self.assertEqual(mock_function.call_count, 1)

    def test_function_always_fails(self):
        mock_function = Mock(side_effect=Exception("Persistent error"))
        mock_function.__name__ = "mock_function"

        decorated_function = retry_deco(3)(mock_function)

        with self.assertRaises(Exception) as _:
            decorated_function()

        self.assertEqual(mock_function.call_count, 3)

    def test_function_no_arguments(self):
        mock_function = Mock(return_value="Success")
        mock_function.__name__ = "mock_function"

        decorated_function = retry_deco(3)(mock_function)

        result = decorated_function()

        self.assertEqual(result, "Success")
        mock_function.assert_called_with()

    def test_function_positional_arguments(self):
        mock_function = Mock(return_value="Success")
        mock_function.__name__ = "mock_function"

        decorated_function = retry_deco(3)(mock_function)

        result = decorated_function(1, 2, 3)

        self.assertEqual(result, "Success")
        mock_function.assert_called_with(1, 2, 3)

    def test_function_keyword_arguments(self):
        mock_function = Mock(return_value="Success")
        mock_function.__name__ = "mock_function"

        decorated_function = retry_deco(3)(mock_function)

        result = decorated_function(a=1, b=2)

        self.assertEqual(result, "Success")
        mock_function.assert_called_with(a=1, b=2)

    def test_function_positional_and_keyword_arguments(self):
        mock_function = Mock(return_value="Success")
        mock_function.__name__ = "mock_function"

        decorated_function = retry_deco(3)(mock_function)

        result = decorated_function(1, 2, a=3, b=4)

        self.assertEqual(result, "Success")
        mock_function.assert_called_with(1, 2, a=3, b=4)

    def test_function_complex_arguments(self):
        mock_function = Mock(return_value="Success")
        mock_function.__name__ = "mock_function"

        complex_arg = {"key1": [1, 2, 3], "key2": {"inner_key": "value"}}

        decorated_function = retry_deco(3)(mock_function)

        result = decorated_function(complex_arg, x=(1, 2, 3))

        self.assertEqual(result, "Success")
        mock_function.assert_called_with(complex_arg, x=(1, 2, 3))

    def test_argument_formatting_no_arguments(self):
        mock_function = Mock(return_value="Success")
        mock_function.__name__ = "mock_function"

        decorated_function = retry_deco(3)(mock_function)

        captured_output = StringIO()
        sys.stdout = captured_output

        result = decorated_function()

        sys.stdout = sys.__stdout__

        self.assertEqual(result, "Success")

        output = captured_output.getvalue()
        expected_output = (
            'run "mock_function" with no arguments, '
            "attempt = 1, "
            "result = Success\n"
        )
        self.assertEqual(output.strip(), expected_output.strip())
