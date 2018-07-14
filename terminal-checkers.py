class CheckerboardState(object):
    """Model keeps track of the checker board.

    columns are labelled a to h (left to right)
    rows are labelled 8 to 1 (top to bottom)
    """
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def get_context_for_row(self, row_number):
        """Returns a dictionary of all of the information needed to draw one row on the board.

        Dictionary will have these keys:
        row: integer, should be between 1 and 8
        selected: column that is currently selected. Can be None.
        pieces: an array up to 8 elements long. Can contain one of these strings.
            None - blank space
            "red" - regular red piece
            "red king" - kinged red piece
            "black" - regular black piece
            "black king" - kinged black piece
            "valid move" - Indicates the unit can move there
        """

        context = {
            "row": row_number,
            "selected": "h",
            "pieces": ["red", None, "black", "valid move", "black king", "red king", None, "valid move", "red"],
        }

        return context

class CheckerboardDisplay(object):
    """Actually displays the checkerboard.
    """
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.board_state = kwargs.get("board_state", None)

    def draw_board(self):
        """Draw the given board.
        """

        # Print column names
        self.draw_column_names()

        # Rows start from 8 on white's side, 1 on the black's side
        for row_number in range(8,0,-1):
            # If there is no board, just print the row number
            if not self.board_state:
                print (row_number)
                continue

            # Ask for the context from the board state.
            context = self.board_state.get_context_for_row(row_number)

            # Add the row number.
            row_display_buffer = "{row_number} ".format(row_number=row_number)

            # For each column,
            for column_index in range(0, 8):
                column_index_to_name = {
                    0: 'a',
                    1: 'b',
                    2: 'c',
                    3: 'd',
                    4: 'e',
                    5: 'f',
                    6: 'g',
                    7: 'h',
                }

                column_name = column_index_to_name[column_index]
                prev_column_name = column_index_to_name.get(column_index - 1, None)
                column_border_shape = "|"
                # Get the border shape based on whether this column was selected.
                if context["selected"] == column_name:
                    column_border_shape = "*"
                elif prev_column_name and context["selected"] == prev_column_name:
                    # We will also have to draw the left side of this column if the previous column was selected.
                    column_border_shape = "*"

                # Get the piece image based on the piece type.
                piece_to_character = {
                    "red":"r",
                    "red king":"R",
                    "black":"b",
                    "black king":"B",
                    "valid move": "!",
                }

                piece_graphic = " "
                if len(context["pieces"]) > column_index:
                    piece_graphic = piece_to_character.get(context["pieces"][column_index], " ")

                column_string = "{border} {piece_graphic} ".format(
                    border = column_border_shape,
                    piece_graphic = piece_graphic
                )

                row_display_buffer += column_string

                # If this is the final column, print the right side as well.
                if column_index == 7:
                    # Get the border shape based on whether this column was selected.
                    if context["selected"] == column_name:
                        row_display_buffer += '*'
                    else:
                        row_display_buffer += '|'


            # Now, print the string.
            print (row_display_buffer)

    def draw_column_names(self):
        print ("    a   b   c   d   e   f   g   h ")

if __name__ == '__main__':
    #keyboard_input = input("What is this?")
    #print ("I'm just echoing what you said: {echo}".format(echo=keyboard_input))

    checkerboard_state = CheckerboardState()

    checkerboard_display = CheckerboardDisplay(
        board_state = checkerboard_state
    )
    checkerboard_display.draw_board()
