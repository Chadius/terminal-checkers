class CheckerboardDisplay(object):
    """Actually displays the checkerboard.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(**kwargs)

    def draw_board(self):
        """Draw the given board.
        """
        print ("Insert drawing here")
        # Rows start from 8 on white's side, 1 on the black's side
        # Columns start from a on the left, g on the right

if __name__ == '__main__':
    #keyboard_input = input("What is this?")
    #print ("I'm just echoing what you said: {echo}".format(echo=keyboard_input))

    checkerboard_display = CheckerboardDisplay()
    checkerboard_display.draw_board()
