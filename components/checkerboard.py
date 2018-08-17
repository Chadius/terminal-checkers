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
        for loc in range(1, 12):
            newchecker = Checker()
            newchecker.set_color("black")
            self.pieces_by_location[loc] = {
                "location": loc,
                "color": newchecker.get_color(),
                "type": newchecker.get_type(),
            }

        # Create the White pieces
        # They inhabit locations 21-32.
        for loc in range(21, 32):
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

# TODO CheckersGame contains Checkerboard
# - knows whose turn it is
# - knows who won
# - knows move history
# - knows valid moves

