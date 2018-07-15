class InvalidLocationException(Exception):
    pass

class TextInput(object):
    @static_method
    def parse_location(string_location):
        """Tries to convert the location and return a dict.
        Throws an InvalidLocationException if it can't interpret.
        """

        # The first character should be a letter.
        
        # The remaining letters should be a number.

        # Return a dict with the row and column.
        return {
            "column": column,
            "row": row,
        }
