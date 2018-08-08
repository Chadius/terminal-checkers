from unittest import TestCase
from unittest.mock import MagicMock

from texthandling.input import TextInput
from texthandling.input import InvalidLocationException

from models.checkerboard import CheckerboardModel

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

class BoardStateTest(TestCase):
    """Make sure the board state is accurate.
    """
    def test_initial_board(self):
        """Confirm the initial board layout is valid.
        """
        checkerboard = CheckerboardModel()
        # Get state
        piece_locations = checkerboard.get_all_piece_locations()

        # Make sure there are 12 Black and 12 White pieces
        black_pieces_count = 0
        white_pieces_count = 0

        for location in piece_locations:
            if piece_locations[location] in ('white man', 'white king'):
                white_pieces_count += 1
            if piece_locations[location] in ('black man', 'black king'):
                black_pieces_count += 1
        self.assertEqual(white_pieces_count, 12)
        self.assertEqual(black_pieces_count, 12)

        # Make sure the Black pieces are in the proper location
        # Make sure the White pieces are in the proper location
        black_piece_locations = {}
        white_piece_locations = {}
        for location in piece_locations:
            if piece_locations[location] in ('white man', 'white king'):
                self.assertFalse(location < 21 or location > 32, "White piece was found at location {loc}".format(loc=location))
                white_piece_locations[location] = piece_locations[location]

            if piece_locations[location] in ('black man', 'black king'):
                self.assertFalse(location < 1 or location > 12, "Black piece was found at location {loc}".format(loc=location))
                black_piece_locations[location] = piece_locations[location]
        self.assertEqual(len(white_piece_locations.keys()), 12, "White pieces not in proper locations. Locations found: {loc}".format(loc=locations))
        self.assertEqual(len(black_piece_locations.keys()), 12, "Black pieces not in proper locations. Locations found: {loc}".format(loc=locations))

        # The game just started - there should not be any kings
        self.assertFalse("white king" in white_piece_locations.values(), "White king found in initial layout: {loc}".format(loc=locations))
        self.assertFalse("black king" in black_piece_locations.values(), "Black king found in initial layout: {loc}".format(loc=locations))

        # Try to record the pieces as a string and check it is correct.
        string_export = checkerboard.export_as_string()
        self.assertEqual(
            string_export,
            "01b02b03b04b05b06b07b08b09b10b11b12b21w22w23w24w25w26w27w28w29w30w31w32w"
        )

    def test_load_string(self):
        """Initialize the checkerboard, using a string.
        Make sure the locations are accurate.
        """
        checkerboard = CheckerboardModel()

        # Create a string to load the pieces
        piece_placement_string = "10w3W29B20b"

        # Reset the board using the string.
        checkerboard.setup_with_string(piece_placement_string)

        # Confirm pieces are in the correct location.
        piece_locations = checkerboard.get_all_piece_locations()
        self.assertEqual(len(piece_locations), 4)
        self.assertEqual(piece_locations[10], "white man")
        self.assertEqual(piece_locations[3], "white king")
        self.assertEqual(piece_locations[20], "black man")
        self.assertEqual(piece_locations[29], "black king")

        # Create another string and reload the table that way.
        piece_placement_string = "15b"

        # Confirm pieces are in the correct location.
        checkerboard.setup_with_string(piece_placement_string)
        self.assertEqual(len(piece_locations), 1)
        self.assertEqual(piece_locations[15], "black man")

    def test_yaml_processing(self):
        """Use YAML strings to save and load the table.
        """
        checkerboard = CheckerboardModel()

        # Set up the board.

        # Export the board state as a YAML string.

        # Make a new board.

        # Digest the YAML string.

        # Make sure the pieces of the two boards are on the same position.
        pass
