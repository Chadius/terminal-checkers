from unittest import TestCase
from unittest.mock import MagicMock

from texthandling.input import TextInput
from texthandling.input import InvalidLocationException

class TextInputTest(TestCase):
    """Confirm you can interpret and understand text commands.
    """
    def setUp(self):
        pass

    def test_parse_location(self):
        """Confirm you understand the string representing the location.
        """

        # TODO: locations should be checkers locations. columns should be letters.
        string_to_location = [
            {
                "input": "a1",
                "column": "a",
                "row" : 1,
            },
            {
                "input": "c4",
                "column": "c",
                "row" : 4,
            },
            {
                "input": "z6",
                "throws_exception": True,
            },
            {
                "input": "8p",
                "throws_exception": True,
            },
            {
                "input": "",
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

# TODO, you'll have to add the official numbers for positions on the board
class BoardValidation(TestCase):
    """Make sure the board is valid.
    """
    def setUp(self):
        # TODO: Create board object
        pass

    def test_initial_board_is_valid(self):
        """Confirm the initial board layout is valid.
        """
        pass

    def test_pieces_must_stay_on_one_color(self):
        """All pieces should be on the "black" squares, like a1.
        """
        pass

    def test_max_one_selected_space(self):
        """No more than one space should be selected.
        """
        pass
