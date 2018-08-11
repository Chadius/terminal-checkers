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

# TODO Checkerboard contains multiple Checkers.
# - knows the size of the board
# - knows checker locations

# TODO CheckersGame contains Checkerboard
# - knows whose turn it is
# - knows who won
# - knows move history
# - knows valid moves
