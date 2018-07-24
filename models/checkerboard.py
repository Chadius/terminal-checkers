class Checker(object):
    """Also called a draught, this is an individual piece on the board.
    """
    def __init__(self, *args, **kwargs):
        self.reset()

    def reset(self):
        self.color = None
        self.is_king = False
        self.is_captured = False
        self.row = None
        self.column = None
        self.board_position = None

class CheckerboardModel(object):
    """
    """

    def __init__(self, *args, **kwargs):
        self.checkers = []
        pass

    def initialize_board(self):
        """Put pieces in the correct places on the board.
        """

        # Clear the old checkers.
        self.checkers = []

        # Add all of the checkers.
        for color in ("black", "white"):
            for index in range(12):
                checker = Checker()
                checker.color = color
                checker.is_king = False
                checker.is_captured = False

                # Black checkers take the first 12 positions.
                if color == "black":
                    checker.board_position = index
                else:
                    # White checkers start with position 21.
                    checker.board_position = 21 + index
                row_column = self.position_to_row_column(checker.board_position)
                checker.row = row_column["row"]
                checker.column = row_column["column"]
        pass

    def is_valid(self):
        """returns True if the board layout is valid.
        """
        pass

    def position_to_row_column(self, position):
        """Convert the position to a row/column pair.
        TODO: Should this be part of texthandling?
        """

        # Figure out what row this is on.
        row = 1 + ((position - 1) / 4)

        # Figure out if it should be in the 1st, 2nd, 3rd or 4th slot on the row.
        slot = ((position -1) % 4)

        # If the row is odd, the 1st slot is on the 2nd column on the board.
        if row % 2 == 1:
            column = 2 + (slot * 2)
        else:
            # If the row is even, the 1st slot is on the 1st column on the board.
            column = 1 + (slot * 2)

        return {
            'row': row,
            'column': column,
        }
