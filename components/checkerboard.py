class Checker(object):
    """Also called a draught, this is an individual piece on the board.
    """
    def __init__(self, *args, **kwargs):
        self.color = None
        self.is_captured = False
        self.is_king = False

    def set_color(self, color):
        """Sets the checker's color.
        Raises a KeyError if it the color is not Black or White.
        """

        lower_color_name = color.lower()

        color_map = {
            "white": "White",
            "black": "Black",
        }

        self.color = color_map[lower_color_name]

    def capture(self):
        """Mark this checker as captured.
        """
        self.is_captured = True

    def promote_to_king(self):
        """Promote this piece and make it a king.
        """
        self.is_king = True

    def get_color(self):
        return self.color

    def get_type(self):
        if self.is_king:
            return "King"
        return "Man"

class Checkerboard(object):
    """ Checkerboard contains multiple Checkers.
    - knows the size of the board
    - knows checker locations
    """
    def __init__(self, *args, **kwargs):
        self.columns = None
        self.rows = None
        self.pieces_by_location = {}
        self.reset_board()

    def reset_board(self):
        """Reset all of the pieces on the board.
        """
        # Set the board to 8 rows and 8 columns.
        self.columns = 8
        self.rows = 8
        self.pieces_by_location = {}

        # Create the Black pieces
        # They inhabit locations 1-12.
        for loc in range(1, 12+1):
            newchecker = Checker()
            newchecker.set_color("black")
            self.pieces_by_location[loc] = {
                "location": loc,
                "color": newchecker.get_color(),
                "type": newchecker.get_type(),
            }

        # Create the White pieces
        # They inhabit locations 21-32.
        for loc in range(21, 32+1):
            newchecker = Checker()
            newchecker.set_color("white")
            self.pieces_by_location[loc] = {
                "location": loc,
                "color": newchecker.get_color(),
                "type": newchecker.get_type(),
            }

    def get_all_pieces_by_location(self):
        return self.pieces_by_location

    def location_to_coordinates(self, location):
        """Convert location to coordinates.
        """

        # If the location is not between 1-32, raise an exception
        if location < 1 or location > 32:
            raise KeyError("Location is invalid, {loc}".format(loc=location))

        # Divide by 8 and add 1 to get the row.
        row = 8 - int((location - 1) / 4)

        # Mod by 4 to get the column position.
        column_position = (location-1) % 4

        # Get the column offset based on the row number.
        if row % 2 == 0:
            column = (column_position * 2) + 2
        else:
            column = (column_position * 2) + 1

        return {
            "row": row,
            "column": column,
        }

class CheckerGame(object):
    """A Game of Checkers tracks the board, the turn and determines valid moves.
    """
    def __init__(self, *args, **kwargs):
        self.board = Checkerboard()
        self.current_turn = None
        self.move_history = []

        self.reset_game()

    def reset_game(self):
        """Resets the game.
        """
        self.current_turn = "White"
        self.move_history = []
        self.board.reset_board()

    def get_current_turn(self):
        return self.current_turn

    def get_move_history(self):
        return self.move_history

    def get_current_legal_moves(self):
        """Look at the current turn and the board to determine all of the legal moves on the board.
        Returns a list of dicts.
        start - Integer containing the start location
        end - Integer containing the end location
        """
        # Whose turn is it, again?
        current_turn = self.current_turn

        # Ask the board for all of the pieces with that color.
        all_pieces = self.board.get_all_pieces_by_location()
        matching_pieces = [ v for k,v in all_pieces.items() if v["color"] == current_turn ]

        # For each piece
        all_legal_moves = []
        for checker_info in matching_pieces:
            # Ask each piece for its legal moves
            legal_moves_for_piece = self.get_legal_moves_for_checker(checker_info)

            # Add all of those locations to the results
            all_legal_moves += legal_moves_for_piece

        # Return all results.
        return all_legal_moves

    def get_legal_moves_for_checker(self, checker_info):
        """Looks at the legal moves for the checker at the given location.
        Returns a list of dicts. See get_current_legal_moves for a description.
        """

        # TODO Get the piece at the given location
        # TODO Get all of its neighboring locations.
        # TODO Man can only move forward.
        # TODO Kings can move forward and backward.
        # TODO Remove any pieces that are not legal.
        # TODO For each neighbor, if the space is blank the piece can move there.
        # TODO If the neighbor is occupied by a checker of its own color, it cannot move there.
        ## TODO Check for jumps!
        return []

    # TODO CheckersGame contains Checkerboard
# - knows whose turn it is
# - knows who won
# - knows move history
# - knows valid moves

