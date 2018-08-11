from unittest import TestCase
from unittest.mock import MagicMock

from texthandling.input import TextInput
from texthandling.input import InvalidLocationException

from components.checkerboard import Checker

class TextInputTest(TestCase):
    """Confirm you can interpret and understand text commands.
    """
    def setUp(self):
        pass

    def test_parse_location(self):
        """Confirm you understand the string representing the location.
        """
        string_to_location = [
            {
                "input": "a1",
                "column": 1,
                "row" : 1,
                "position": 29,
            },
            {
                "input": "c5",
                "column": 3,
                "row" : 5,
                "position": 14,
            },
            {
                "input": "z6",
                "throws_exception": True,
            },
            {
                "input": "8",
                "column": 7,
                "row" : 7,
                "position": 8,
            },
            {
                "input": "",
                "throws_exception": True,
            },
            {
                "input": "a4",
                "throws_exception": True,
            },
        ]

        for datum in string_to_location:
            if "throws_exception" in datum and datum["throws_exception"]:
                exception_raised = False
                try:
                    TextInput.parse_location(datum["input"])
                except InvalidLocationException:
                    exception_raised = True
                self.assertTrue(exception_raised, "InvalidLocationException was not raised while testing: {context}".format(context=datum))
            else:
                location = TextInput.parse_location(datum["input"])
                self.assertEqual(
                    location["row"],
                    datum["row"],
                    "Expected row {expected_row} but got {actual_row} instead. Context: {context}".format(
                        expected_row = datum["row"],
                        actual_row = location["row"],
                        context = datum
                    )
                )
                self.assertEqual(
                    location["column"],
                    datum["column"],
                    "Expected column {expected_column} but got {actual_column} instead. Context: {context}".format(
                        expected_column = datum["column"],
                        actual_column = location["column"],
                        context = datum
                    )
                )
                self.assertEqual(
                    location["position"],
                    datum["position"],
                    "Expected position {expected_position} but got {actual_position} instead. Context: {context}".format(
                        expected_position = datum["position"],
                        actual_position = location["position"],
                        context = datum
                    )
                )

class CheckerTest(TestCase):
    """Check the Checker's model and controller actions.
    """

    def setUp(self):
        self.checker = Checker()

    def test_checker_color(self):
        """Confirm the checker knows its color.
        """

        # Checkers do not have colors when they are created.
        self.assertIsNone(self.checker.color)

        # Set the color to black and confirm the color changed
        self.checker.set_color("Black")
        self.assertEqual(self.checker.color, "Black")

        # Set the color to white and confirm the color changed
        self.checker.set_color("white")
        self.assertEqual(self.checker.color, "White")

        # Set the color to something invalid. An exception should be raised.
        exception_raised = False
        try:
            self.checker.set_color("banana")
        except KeyError:
            exception_raised = True
        self.assertTrue(exception_raised, "KeyError was not raised while setting color to banana")

    def test_checker_captured(self):
        """Confirm the checker can be captured.
        """
        # The checker starts off as not captured.
        self.assertFalse(self.checker.is_captured)

        # Mark the piece as captured and confirm it was.
        self.checker.capture()
        self.assertTrue(self.checker.is_captured)

    def test_checker_promote(self):
        """Confirm the checker knows it can be promoted
        """

        # The checker is not a king.
        self.assertFalse(self.checker.is_king)

        # Promote the piece.
        self.checker.promote_to_king()
        self.assertTrue(self.checker.is_king)
