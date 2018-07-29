class InvalidLocationException(Exception):
    pass

class TextInput(object):
    @staticmethod
    def parse_location(string_location):
        """Tries to convert the location and return a dict.
        Throws an InvalidLocationException if it can't interpret.
        """
        try:
            return TextInput.parse_chess_location(string_location)
        except InvalidLocationException:
            raise

    @staticmethod
    def parse_location(string_location):
        """Given a string representing a checkers location, return a dict with the row and column.
        Raises a InvalidLocationException if it fails.
        """

        # Convert it into an integer. Raise an error if it fails.
        try:
            position = int(string_location)
        except ValueError:
            coords = TextInput.parse_chess_position(string_location)

            # Make sure the coordinates are reachable on a checker board.
            # If the column is 1 3 5 7 , then the row must be odd.
            if coords['column'] % 2 == 1 and coords['row'] % 2 == 0:
                raise InvalidLocationException
            # If the column is 2 4 6 8 , then the row must be even.
            if coords['column'] % 2 == 0 and coords['row'] % 2 == 1:
                raise InvalidLocationException

            # Calculate the position based on the row and column.
            # Because chess and checkers counting row directions are reversed, count down from 8 and multiply by 4.
            chess_position = (8 - coords['row']) * 4
            # Subtract the column by 1, then Divide by 2 and add 1 again to get the column position on the row.
            chess_position += ((coords['column'] - 1) / 2) + 1

            return {
                "row" : coords['row'],
                "column" : coords['column'],
                "position" : chess_position,
            }

        # position should be between 1 and 32 (inclusive)
        if position < 1 or position > 32:
            raise InvalidPositionException

        # Position starts at 1, so subtract 1 to make the math easy.
        math_position = position -1

        # Mod by 4 to get the slot on the given row.
        slot = (math_position % 4) + 1

        # Divide by 4 to figure out how many rows from the top. (Row 8 is the highest row)
        row = 8 - int(math_position / 4)

        # If the row is even, the column is in the 2 * slot column
        if row % 2 == 0:
            column = 2 * slot
        else:
            # If the row is odd, the column is in the 2 * slot - 1 column
            column = 2 * slot - 1

        return {
            "row" : row,
            "column" : column,
            "position" : position,
        }

    @staticmethod
    def parse_chess_position(string_location):
        """Given a string representing a location on a chess board, try to return the row and column.
        Raises a InvalidLocationException if it fails.
        """
        # The first character should be a letter.
        try:
            raw_column = string_location[0]
        except IndexError:
            raise InvalidLocationException

        column_character_to_column = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "f": 6,
            "g": 7,
            "h": 8,

            "A": 1,
            "B": 2,
            "C": 3,
            "D": 4,
            "E": 5,
            "F": 6,
            "G": 7,
            "H": 8,

            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
        }

        column = None
        try:
            column = column_character_to_column[raw_column]
        except KeyError:
            raise InvalidLocationException

        # The remaining letters should be a number.
        try:
            raw_row = string_location[1:]
        except IndexError:
            raise InvalidLocationException

        try:
            row = int(raw_row)
        except ValueError:
            raise InvalidLocationException

        # Return a dict with the row and column.
        return {
            "column": column,
            "row": row,
        }
