from unittest import TestCase
from unittest.mock import MagicMock

from texthandling.input import TextInput
from texthandling.input import InvalidLocationException

from components.checkerboard import Checker
from components.checkerboard import Checkerboard
from components.checkerboard import CheckerGame

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

class CheckerboardTest(TestCase):
    """Check the Checkerboard's model and controller actions.
    """
    def setUp(self):
        self.board = Checkerboard()

    def test_dimensions(self):
        """Confirm it's the default size, 8x8
        """
        self.assertEqual(self.board.columns, 8)
        self.assertEqual(self.board.rows, 8)

    def test_checker_locations(self):
        """Make sure the checkers are in the correct locations.
        """
        self.board.reset_board()

        all_piece_locations = self.board.get_all_pieces_by_location()

        # Black pieces
        for loc in range(1, 12+1):
            self.assertTrue(loc in all_piece_locations, "Can't find location {loc}".format(loc=loc))
            self.assertEqual(all_piece_locations[loc]["location"], loc)
            self.assertEqual(all_piece_locations[loc]["color"], "Black")
            self.assertEqual(all_piece_locations[loc]["type"], "Man")

        # White pieces
        for loc in range(21, 32+1):
            self.assertTrue(loc in all_piece_locations, "Can't find location {loc}".format(loc=loc))
            self.assertEqual(all_piece_locations[loc]["location"], loc)
            self.assertEqual(all_piece_locations[loc]["color"], "White")
            self.assertEqual(all_piece_locations[loc]["type"], "Man")

    def test_coordinates_to_location(self):
        """ Test you can convert coordinates to a location.
        """
        location_to_coordinates = {
            1 : { "row": 8, "column": 2, },
            2 : { "row": 8, "column": 4, },
            3 : { "row": 8, "column": 6, },
            4 : { "row": 8, "column": 8, },
            5 : { "row": 7, "column": 1, },
            6 : { "row": 7, "column": 3, },
            7 : { "row": 7, "column": 5, },
            8 : { "row": 7, "column": 7, },
            9 : { "row": 6, "column": 2, },
            10: { "row": 6, "column": 4, },
            11: { "row": 6, "column": 6, },
            12: { "row": 6, "column": 8, },
            13: { "row": 5, "column": 1, },
            14: { "row": 5, "column": 3, },
            15: { "row": 5, "column": 5, },
            16: { "row": 5, "column": 7, },
            17: { "row": 4, "column": 2, },
            18: { "row": 4, "column": 4, },
            19: { "row": 4, "column": 6, },
            20: { "row": 4, "column": 8, },
            21: { "row": 3, "column": 1, },
            22: { "row": 3, "column": 3, },
            23: { "row": 3, "column": 5, },
            24: { "row": 3, "column": 7, },
            25: { "row": 2, "column": 2, },
            26: { "row": 2, "column": 4, },
            27: { "row": 2, "column": 6, },
            28: { "row": 2, "column": 8, },
            29: { "row": 1, "column": 1, },
            30: { "row": 1, "column": 3, },
            31: { "row": 1, "column": 5, },
            32: { "row": 1, "column": 7, },
        }

        for loc in location_to_coordinates:
            coords = location_to_coordinates[loc]
            location = self.board.coordinates_to_location(coords)
            self.assertEqual(
                location,
                loc,
                "Location for coordinates at row {row} and column {col} do not match. Expected {expected}, Actual {actual}".format(
                    row = coords["row"],
                    col = coords["column"],
                    expected = loc,
                    actual = location,
                )
            )

    def test_location_to_coordinates(self):
        """Confirm the location correctly translates to coordinates.
        """
        location_to_coordinates = {
            1 : { "row": 8, "column": 2, },
            2 : { "row": 8, "column": 4, },
            3 : { "row": 8, "column": 6, },
            4 : { "row": 8, "column": 8, },
            5 : { "row": 7, "column": 1, },
            6 : { "row": 7, "column": 3, },
            7 : { "row": 7, "column": 5, },
            8 : { "row": 7, "column": 7, },
            9 : { "row": 6, "column": 2, },
            10: { "row": 6, "column": 4, },
            11: { "row": 6, "column": 6, },
            12: { "row": 6, "column": 8, },
            13: { "row": 5, "column": 1, },
            14: { "row": 5, "column": 3, },
            15: { "row": 5, "column": 5, },
            16: { "row": 5, "column": 7, },
            17: { "row": 4, "column": 2, },
            18: { "row": 4, "column": 4, },
            19: { "row": 4, "column": 6, },
            20: { "row": 4, "column": 8, },
            21: { "row": 3, "column": 1, },
            22: { "row": 3, "column": 3, },
            23: { "row": 3, "column": 5, },
            24: { "row": 3, "column": 7, },
            25: { "row": 2, "column": 2, },
            26: { "row": 2, "column": 4, },
            27: { "row": 2, "column": 6, },
            28: { "row": 2, "column": 8, },
            29: { "row": 1, "column": 1, },
            30: { "row": 1, "column": 3, },
            31: { "row": 1, "column": 5, },
            32: { "row": 1, "column": 7, },
        }

        for loc in location_to_coordinates:
            coordinate = self.board.location_to_coordinates(loc)
            self.assertEqual(
                coordinate,
                location_to_coordinates[loc],
                "Coordinates for location {location} do not match. Expected {expected}, Actual {actual}".format(
                    location = loc,
                    expected = location_to_coordinates[loc],
                    actual = coordinate,
                )
            )

    def test_get_piece_not_captured(self):
        """ You can read the board and see non-captured pieces.
        """
        # Reset the board
        self.board.reset_board()

        # Verify you see a captured piece there.
        piece = self.board.get_piece(1)
        self.assertEqual(piece["color"], "Black")

        # Capture the piece.
        self.board.capture_piece(1)

        # Verify you don't see a captured piece there.
        piece = self.board.get_piece(1)
        self.assertIsNone(piece)

        # Verify the piece isn't in the "all" pieces
        all_piece_locations = self.board.get_all_pieces_by_location()
        self.assertFalse(1 in all_piece_locations)

    def test_load_board_formation(self):
        """ You can load board positions.
        """

        # Place pieces using a list of pieces.
        self.board.arrange_board({
            11: {
                "color": "white",
                "type" : "man",
            },
            8: {
                "color": "black",
                "type" : "man",
            },
            4: {
                "color": "black",
                "type" : "king",
            },
        })

        # Make sure there are 3 pieces.
        all_piece_locations = self.board.get_all_pieces_by_location()
        self.assertEqual(len(all_piece_locations.keys()), 3)

        # Make sure the correct pieces are at the correct spots.
        self.assertTrue(8 in all_piece_locations)
        self.assertEqual(all_piece_locations[8]["location"], 8)
        self.assertEqual(all_piece_locations[8]["color"], "Black")
        self.assertEqual(all_piece_locations[8]["type"], "Man")

        self.assertTrue(4 in all_piece_locations)
        self.assertEqual(all_piece_locations[4]["location"], 4)
        self.assertEqual(all_piece_locations[4]["color"], "Black")
        self.assertEqual(all_piece_locations[4]["type"], "King")

        self.assertTrue(11 in all_piece_locations)
        self.assertEqual(all_piece_locations[11]["location"], 11)
        self.assertEqual(all_piece_locations[11]["color"], "White")
        self.assertEqual(all_piece_locations[11]["type"], "Man")

class CheckerGameTest(TestCase):
    """Check the CheckerGame's model and controller actions.
    """

    def setUp(self):
        self.game = CheckerGame()

    def test_current_turn(self):
        """White moves first.
        """
        self.assertEqual(self.game.get_current_turn(), "White")

    def test_move_history_starts_blank(self):
        """Confirm the move history starts blank.
        """
        history = self.game.get_move_history()
        self.assertEqual(history, [])

    def test_legal_moves_for_white(self):
        """Return all of the legal moves the White team can perform.
        """
        game_moves = self.game.get_current_legal_moves()

        self.assertEqual(len(game_moves), 7)

        expected_moves_by_start_location = {
            21 : [17],
            22 : [17, 18],
            23 : [18, 19],
            24 : [19, 20],
        }

        actual_moves_by_start_location = {}

        # Make sure every reported legal move is in the list of expected moves.
        for move in game_moves:
            # Make sure the start point is legal.
            start_loc = move["start"]
            self.assertTrue(
                start_loc in expected_moves_by_start_location,
                "No legal move starts with {loc}".format(
                    loc=start_loc
                )
            )

            if not start_loc in actual_moves_by_start_location:
                actual_moves_by_start_location[start_loc] = []

            # Make sure the same move was not added twice.
            end_loc = move["end"]
            self.assertFalse(
                end_loc in actual_moves_by_start_location[start_loc],
                "{start} - {end} should not be a legal move.".format(
                    start=start_loc,
                    end=end_loc,
                )
            )

            actual_moves_by_start_location[start_loc].append(end_loc)

        # Make sure every expected move has been accounted for.
        for start_loc in expected_moves_by_start_location:
            self.assertTrue(
                start_loc in actual_moves_by_start_location,
                "{start} not found in actual moves".format(
                    start = start_loc
                )
            )

            # Make sure they have the same number of end points.
            self.assertEqual(
                len(actual_moves_by_start_location[start_loc]),
                len(expected_moves_by_start_location[start_loc]),
                "Legal moves starting with {start}: Expected {expected}, Actual {actual}".format(
                    start = start_loc,
                    expected = len(expected_moves_by_start_location[start_loc]),
                    actual = len(actual_moves_by_start_location[start_loc]),
                )
            )

            # Both lists have the same contents.

    def test_end_turn(self):
        """Tests that you can change turns.
        """
        self.assertEqual(self.game.get_current_turn(), "White")
        self.game.end_turn()
        self.assertEqual(self.game.get_current_turn(), "Black")
        self.game.end_turn()
        self.assertEqual(self.game.get_current_turn(), "White")

    def test_legal_moves_for_black(self):
        """Return all of the legal moves the Black team can perform.
        """
        self.game.end_turn()

        game_moves = self.game.get_current_legal_moves()

        self.assertEqual(len(game_moves), 7)

        expected_moves_by_start_location = {
            9 : [13, 14],
            10 : [14, 15],
            11 : [15, 16],
            12 : [16],
        }

        actual_moves_by_start_location = {}

        # Make sure every reported legal move is in the list of expected moves.
        for move in game_moves:
            # Make sure the start point is legal.
            start_loc = move["start"]
            self.assertTrue(
                start_loc in expected_moves_by_start_location,
                "No legal move starts with {loc}".format(
                    loc=start_loc
                )
            )

            if not start_loc in actual_moves_by_start_location:
                actual_moves_by_start_location[start_loc] = []

            # Make sure the same move was not added twice.
            end_loc = move["end"]
            self.assertFalse(
                end_loc in actual_moves_by_start_location[start_loc],
                "{start} - {end} should not be a legal move.".format(
                    start=start_loc,
                    end=end_loc,
                )
            )

            actual_moves_by_start_location[start_loc].append(end_loc)

        # Make sure every expected move has been accounted for.
        for start_loc in expected_moves_by_start_location:
            self.assertTrue(
                start_loc in actual_moves_by_start_location,
                "{start} not found in actual moves".format(
                    start = start_loc
                )
            )

            # Make sure they have the same number of end points.
            self.assertEqual(
                len(actual_moves_by_start_location[start_loc]),
                len(expected_moves_by_start_location[start_loc]),
                "Legal moves starting with {start}: Expected {expected}, Actual {actual}".format(
                    start = start_loc,
                    expected = len(expected_moves_by_start_location[start_loc]),
                    actual = len(actual_moves_by_start_location[start_loc]),
                )
            )

            # Both lists have the same contents.

class JumpingPieceTests(TestCase):
    # Verifies the board can detect jumps.
    # S = Start point
    # B = Black piece
    # W = White piece
    # L = Where the Start piece Lands after jumping
    # Most of these tests use a White piece.

    def setUp(self):
        self.game = CheckerGame()

    def test_peek(self):
        """Tests the peek functionality.
        """
        # |-|-|L|
        # |-|B|-|
        # |S|-|-|
        # White piece at S can jump up and right
        self.game.board.arrange_board({
            11: {
                "color": "white",
                "type" : "man",
            },
            8: {
                "color": "black",
                "type" : "man",
            },
        })

        # Peek white from location 11, to the right - should see a black piece
        peek_item = self.game.board.peek(
            location = 11,
            spaces = 1,
            direction = "blackright"
        )
        self.assertEqual(
            peek_item,
            {
                "offboard": False,
                "empty": False,
                "color": "Black",
                "type": "Man",
                "location": 8,
            }
        )

        # Peek white from location 11, to the left - should see an empty square
        peek_item = self.game.board.peek(
            location = 11,
            spaces = 1,
            direction = "blackleft"
        )
        self.assertEqual(
            peek_item,
            {
                "offboard": False,
                "empty": True,
                "color": "",
                "type": "",
                "location": 7,
            }
        )

        # Peek black from location 8, to the left - should see a white piece square
        peek_item = self.game.board.peek(
            location = 8,
            spaces = 1,
            direction = "whiteleft"
        )
        self.assertEqual(
            peek_item,
            {
                "offboard": False,
                "empty": False,
                "color": "White",
                "type": "Man",
                "location": 11,
            }
        )

        # Peek white from location 4 - should get an offboard location
        peek_item = self.game.board.peek(
            location = 4,
            spaces = 1,
            direction = "blackleft"
        )
        self.assertEqual(
            peek_item,
            {
                "offboard": True,
                "empty": False,
                "color": "",
                "type": "",
                "location": None,
            }
        )

        # Peek white from location 11, 3 spaces - should get an offboard location
        peek_item = self.game.board.peek(
            location = 11,
            spaces = 3,
            direction = "blackright"
        )
        self.assertEqual(
            peek_item,
            {
                "offboard": True,
                "empty": False,
                "color": "",
                "type": "",
                "location": None,
            }
        )

    def test_white_jump_right(self):
        # |-|-|L|
        # |-|b|-|
        # |S|-|-|
        # White piece at S can jump up and right
        self.game.board.arrange_board({
            11: {
                "color": "white",
                "type" : "man",
            },
            8: {
                "color": "black",
                "type" : "man",
            },
        })

        # Ask the White team for all moves
        legal_moves = self.game.get_current_legal_moves()

        # The piece MUST jump
        expected_moves = [{
            "start": 11,
            "jumps_over": [8],
            "lands": [4],
            "end": 4,
        }]

        self.assertEqual(expected_moves, legal_moves)

    def test_white_jump_left(self):
        # |L|-|-|
        # |-|b|-|
        # |-|-|S|
        # White piece at S can jump up and left.
        self.game.board.arrange_board({
            12: {
                "color": "white",
                "type" : "man",
            },
            8: {
                "color": "black",
                "type" : "man",
            },
        })

        # Ask the White team for all moves
        legal_moves = self.game.get_current_legal_moves()

        # The piece MUST jump
        expected_moves = [{
            "start": 12,
            "jumps_over": [8],
            "lands": [3],
            "end": 3,
        }]

        self.assertEqual(expected_moves, legal_moves)

    def test_black_jump(self):
        # |S|-|-|
        # |-|w|-|
        # |-|-|L|
        # Black piece at S can jump.
        self.game.board.arrange_board({
            3: {
                "color": "black",
                "type" : "man",
            },
            8: {
                "color": "white",
                "type" : "man",
            },
        })

        # Ask the Black team for all moves
        self.game.end_turn()
        legal_moves = self.game.get_current_legal_moves()

        # The piece MUST jump
        expected_moves = [{
            "start": 3,
            "jumps_over": [8],
            "lands": [12],
            "end": 12,
        }]

        self.assertEqual(expected_moves, legal_moves)

    def test_white_cannot_jump_same_color(self):
        # |-|-|-|
        # |-|w|-|
        # |S|-|-|
        # White piece at S cannot jump, the jumped piece is the same color.
        self.game.board.arrange_board({
            11: {
                "color": "white",
                "type" : "man",
            },
            8: {
                "color": "white",
                "type" : "man",
            },
        })

        # Ask the White team for all moves
        legal_moves = self.game.get_current_legal_moves()

        # White piece can't jump so they just move 1 square
        expected_moves = [
            {
                "start": 11,
                "end": 7,
            },
            {
                "start": 8,
                "end": 4,
            },
            {
                "start": 8,
                "end": 3,
            },
        ]


        self.assertEqual(len(expected_moves), len(legal_moves))
        for expected_move in expected_moves:
            self.assertTrue(expected_move in legal_moves)

    def test_white_cannot_jump_offboard_column(self):
        # |-|-|-|
        # |-|-|b|
        # |-|S|-|
        # S piece cannot jump because they would land in an offboard column.
        self.game.board.arrange_board({
            16: {
                "color": "white",
                "type" : "man",
            },
            12: {
                "color": "black",
                "type" : "man",
            },
        })

        # Ask the White team for all moves
        legal_moves = self.game.get_current_legal_moves()

        # White piece can't jump so they just move 1 square
        expected_moves = [
            {
                "start": 16,
                "end": 11,
            },
        ]

        self.assertEqual(expected_moves, legal_moves)

    def test_white_cannot_jump_offboard_row(self):
        # |-|b|-|
        # |S|-|-|
        # |-|-|-|
        # S piece cannot jump because they would land in an invalid row.
        self.game.board.arrange_board({
            7: {
                "color": "white",
                "type" : "man",
            },
            3: {
                "color": "black",
                "type" : "man",
            },
        })

        # Ask the White team for all moves
        legal_moves = self.game.get_current_legal_moves()

        # White piece can't jump so they just move 1 square
        expected_moves = [
            {
                "start": 7,
                "end": 2,
            },
        ]

        self.assertEqual(expected_moves, legal_moves)

    def test_white_cannot_jump_landing_blocked(self):
        # |-|-|b|
        # |-|b|-|
        # |S|-|-|
        # S piece cannot jump because the landing is blocked.
        self.game.board.arrange_board({
            11: {
                "color": "white",
                "type" : "man",
            },
            8: {
                "color": "black",
                "type" : "man",
            },
            4: {
                "color": "black",
                "type" : "man",
            },
        })

        # Ask the White team for all moves
        legal_moves = self.game.get_current_legal_moves()

        # The landing location is blocked, so the piece will move normally
        expected_moves = [{
            "start": 11,
            "end": 7,
        }]

        self.assertEqual(expected_moves, legal_moves)

    def test_white_can_jump_multiple_times(self):
        # |-|-|-|-|L|
        # |-|-|-|b|-|
        # |-|-|l|-|-|
        # |-|b|-|-|-|
        # |S|-|-|-|-|
        # Multijumps are possible. S will jump to l and then L.
        self.game.board.arrange_board({
            18: {
                "color": "white",
                "type" : "man",
            },
            15: {
                "color": "black",
                "type" : "man",
            },
            8: {
                "color": "black",
                "type" : "man",
            },
        })

        # Ask the White team for all moves
        legal_moves = self.game.get_current_legal_moves()

        # The piece must jump multiple times in a single move
        expected_moves = [{
            "start": 18,
            "jumps_over": [15, 8],
            "lands": [11, 4],
            "end": 4,
        }]

        self.assertEqual(expected_moves, legal_moves)

    def test_white_can_choose_jumps(self):
        # |1|-|-|-|2|
        # |-|b|-|b|-|
        # |-|-|S|-|-|
        # A white piece can choose between multiple possible jumps.

        self.game.board.arrange_board({
            11: {
                "color": "white",
                "type" : "man",
            },
            7: {
                "color": "black",
                "type" : "man",
            },
            8: {
                "color": "black",
                "type" : "man",
            },
        })

        # Ask the White team for all moves
        legal_moves = self.game.get_current_legal_moves()

        # The White piece has 2 potential moves. Each of them are a jump.
        expected_moves = [
            {
                "start": 11,
                "jumps_over": [7],
                "lands": [2],
                "end": 2,
            },
            {
                "start": 11,
                "jumps_over": [8],
                "lands": [4],
                "end": 4,
            },
        ]

        self.assertEqual(len(expected_moves), len(legal_moves))
        for expected_move in expected_moves:
            self.assertTrue(expected_move in legal_moves)

    def test_white_can_choose_branching_multijump(self):
        # |1|-|-|-|2|
        # |-|b|-|b|-|
        # |-|-|l|-|-|
        # |-|b|-|-|-|
        # |S|-|-|-|-|
        # A piece can make different decisions during a multijump.
        self.game.board.arrange_board({
            18: {
                "color": "white",
                "type" : "man",
            },
            15: {
                "color": "black",
                "type" : "man",
            },
            8: {
                "color": "black",
                "type" : "man",
            },
            7: {
                "color": "black",
                "type" : "man",
            },
        })

        # Ask the White team for all moves
        legal_moves = self.game.get_current_legal_moves()

        # The White piece must jump over the black piece at 15.
        # When it lands on 11, it must choose between jumping over 7 or 8.
        expected_moves = [
            {
                "start": 18,
                "jumps_over": [15, 8],
                "lands": [11, 4],
                "end": 4,
            },
            {
                "start": 18,
                "jumps_over": [15, 7],
                "lands": [11, 2],
                "end": 2,
            },
        ]

        self.assertEqual(len(expected_moves), len(legal_moves))
        for expected_move in expected_moves:
            self.assertTrue(expected_move in legal_moves)
