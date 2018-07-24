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

        # TODO Convert it into an integer. Raise an error if it fails.

        # TODO Copy code from your board stuff.
        pass

    @staticmethod
    def parse_chess_location(string_location):
        """Given a string representing a location on a chess board, try to return the row and column.
        Raises a InvalidLocationException if it fails.
        """
        # The first character should be a letter.
        try:
            raw_column = string_location[0]
        except IndexError:
            raise InvalidLocationException

        column_character_to_column = {
            "a": "a",
            "b": "b",
            "c": "c",
            "d": "d",
            "e": "e",
            "f": "f",
            "g": "g",
            "h": "h",

            "A": "a",
            "B": "b",
            "C": "c",
            "D": "d",
            "E": "e",
            "F": "f",
            "G": "g",
            "H": "h",

            "1": "a",
            "2": "b",
            "3": "c",
            "4": "d",
            "5": "e",
            "6": "f",
            "7": "g",
            "8": "h",
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
