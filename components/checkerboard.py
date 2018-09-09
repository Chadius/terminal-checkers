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

    def change_is_king(self, is_king):
        """Change this piece's king status.
        """
        self.is_king = is_king

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
        self.all_checkers = []

    def reset_board(self):
        """Reset all of the pieces on the board.
        """
        # Set the board to 8 rows and 8 columns.
        self.columns = 8
        self.rows = 8
        self.pieces_by_location = {}
        self.all_checkers = []

        # Create the Black pieces
        # They inhabit locations 1-12.
        for loc in range(1, 12+1):
            newchecker = Checker()
            newchecker.set_color("black")
            self.pieces_by_location[loc] = newchecker
            self.all_checkers.append(newchecker)

        # Create the White pieces
        # They inhabit locations 21-32.
        for loc in range(21, 32+1):
            newchecker = Checker()
            newchecker.set_color("white")
            self.pieces_by_location[loc] = newchecker
            self.all_checkers.append(newchecker)

    def arrange_board(self, piece_by_location):
        """Reset the board and rearrange the pieces.
        The key is the location.
        The value is a dict.
        type
        color
        """

        # Clear all of the pieces by location.
        self.all_checkers = []
        self.pieces_by_location = {}

        # For each location
        for location, description in piece_by_location.items():
            # Get the next captured piece
            cap_piece = Checker()

            # Set its color and type
            cap_piece.set_color(description["color"])

            checker_type = description["type"].lower()
            if checker_type == "king":
                cap_piece.promote_to_king()
            else:
                cap_piece.change_is_king(False)

            # Set the piece location
            self.pieces_by_location[location] = cap_piece

    def get_all_pieces_by_location(self):
        """Returns a dict mapping locations with checkers
        to a dict descibing them.

        location
        color
        type
        """
        pieces_description = {}

        for loc, checker in self.pieces_by_location.items():
            pieces_description[loc] = {
                "location": loc,
                "color": checker.get_color(),
                "type": checker.get_type(),
            }

        return pieces_description

    def location_to_coordinates(self, location):
        """Convert location to coordinates.
        row is 1-8 (Row 1 is on Black's side, Row 8 is on White's side)
        column is 1-8
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

    def coordinates_to_location(self, coordinates):
        """Convert coordinates to location.
        Returns None if there is no possible location.
        """
        row = coordinates["row"]
        col = coordinates["column"]

        # Make sure the row and columns are within the rows and columns.
        if row < 1 or row > self.rows:
            return None

        if col < 1 or col > self.columns:
            return None

        # If the row is even, make sure the column is even
        if row % 2 == 0 and col % 2 != 0:
            return None

        # If the row is odd, make sure the column is odd
        if row % 2 != 0 and col % 2 == 0:
            return None

        # Figure out the location range based on the row.
        location = (8 - row) * 4

        # Convert the column to a range from 0-3 and add it to the row location range.
        location += int((col - 1)  / 2) + 1

        # Return the location.
        return location

    def get_piece(self, location):
        """Returns a dict describing the checker found at the given location.
        Returns None if no piece is at the location OR the checker is captured.
        """

        # Get a description
        pieces_description = self.get_all_pieces_by_location()

        # See if there is no piece at this location.
        if not location in pieces_description:
            return None

        # There is a checker here.
        found_checker = pieces_description[location]

        # return the description
        return found_checker

    def capture_piece(self, location):
        """Capture the piece found at the given location.
        Returns True if successful.
        """
        # Is there a piece at that location?
        if not location in self.pieces_by_location:
            return False

        # Mark the piece as captured.
        checker = self.pieces_by_location[location]
        checker.capture()

        # Remove from the board.
        del[self.pieces_by_location[location]]
        return True

    def peek(self, location, direction, spaces):
        """Starting from location, move in a direction by a number of spaces and return the piece found there.

        location = starting location
        spaces = number of spaces to look ahead
        direction = "blackright", "blackleft", "whiteright" or "whiteleft". This assumes Black is on top and White is on the bottom.

        returns a dict.
        offboard: True if the peek location is off the board in an invalid position.
        empty: True if the peek location is valid but no piece is there.
        color: checker color.
        type: "Man" or "King"
        """

        peek_description = {
            "offboard": False,
            "empty": False,
            "color": "",
            "type": "",
            "location": None,
        }

        # Validate the direction.
        vertical = {
            "blackright": 1,
            "blackleft": 1,
            "whiteright": -1,
            "whiteleft": -1,
        }
        look_up = vertical[direction]

        horizontal = {
            "blackright": 1,
            "blackleft": -1,
            "whiteright": 1,
            "whiteleft": -1,
        }
        look_right = horizontal[direction]

        # Convert the location to coordinates.
        coordinates = self.location_to_coordinates(location)

        # Based on the direction, change coordinates to the number of squares.
        coordinates["row"] += look_up * spaces
        coordinates["column"] += look_right * spaces

        # Convert back to a location.
        new_location = self.coordinates_to_location(coordinates)

        # Indicate if it's offscreen
        if new_location == None:
            peek_description["offboard"] = True
            return peek_description

        peek_description["location"] = new_location

        # If there is a piece, fill in the color and type.
        all_pieces = self.get_all_pieces_by_location()
        if new_location in all_pieces:
            peek_description["color"] = all_pieces[new_location]["color"]
            peek_description["type"] = all_pieces[new_location]["type"]
            return peek_description

        # Otherwise return an empty space.
        peek_description["empty"] = True
        return peek_description

    def get_opposite_direction(self, direction):
        """Returns a string noting the opposite direction.
        left/right are opposites.
        black/right are opposites, noting which side the pieces start on.
        compound directions (examplel: blackright, whiteleft) can be used.
        Returns None if no direction can be found.
        """
        direction_opposites = {
            "black" : "white",
            "white" : "black",
            "left" : "right",
            "right" : "left",
            "blackleft" : "whiteright",
            "blackright" : "whiteleft",
            "whiteleft" : "blackright",
            "whiteright" : "blackleft",
        }

        return direction_opposites.get(direction, None)

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

    def end_turn(self):
        """Swaps between White and Black teams.
        """
        if self.current_turn == "White":
            self.current_turn = "Black"
        else:
            self.current_turn = "White"

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
            legal_moves_for_piece = self.get_legal_moves_for_checker(checker_info, all_pieces)

            # Add all of those locations to the results
            all_legal_moves += legal_moves_for_piece

        # Return all results.
        return all_legal_moves

    def get_legal_moves_for_checker(self, checker_info, all_pieces_info, previous_jump_direction = None):
        """Looks at the legal moves for the checker at the given location.
        Returns a list of dicts. See get_current_legal_moves for a description.
        """

        # Get the piece at the given location
        color = checker_info["color"]
        checker_type = checker_info["type"]
        start_location = checker_info["location"]
        checker_desc = color + " " + checker_type

        print ("Starting location: {loc}".format(loc=start_location)) # TODO

        # Generate directions for this piece.
        directions_by_description = {
            "White Man": ['blackright', 'blackleft'],
            "White King": ['blackright', 'blackleft', 'whiteright', 'whiteleft'],
            "Black Man": ['whiteright', 'whiteleft'],
            "Black King": ['whiteright', 'whiteleft', 'blackright', 'blackleft', ]
        }

        # Remove any directions you've already jumped from.
        directions = directions_by_description[checker_desc]

        if previous_jump_direction:
            opposite_jump_direction = self.board.get_opposite_direction(previous_jump_direction)
            directions = [d for d in directions if d != opposite_jump_direction]
        print (', '.join(directions)) # TODO
        # For each direction
        legal_moves_without_jumps = []
        legal_moves_with_jumps = []
        for direction in directions:
            # Peek 1 square.
            info = self.board.peek(start_location, direction, 1)

            # If the square is unoccupied and on the board, add this move to the list and move on.
            if info["empty"] and not info["offboard"]:
                print ("{loc} is empty, adding to legal moves".format(loc=info["location"])) # TODO
                legal_moves_without_jumps.append({
                    "start": start_location,
                    "end": info["location"],
                })

            # If the square belongs to a different color, we may be able to jump!
            if not(info["offboard"] or info["empty"]) and info["color"] != color:
                print ("{loc} has a different color, maybe I can jump {dir}".format(loc=info["location"], dir=direction)) # TODO
                # Peek 2 squares away and make sure it's an empty space you can land on.
                two_square_info = self.board.peek(start_location, direction, 2)
                print ("Peeking at landing spot: {spot}".format(spot=two_square_info)) # TODO
                if two_square_info["empty"] and not two_square_info["offboard"]:
                    print ("Destination is empty and on the board. I need to check for multiple jumps.") #TODO

                    # We need to check for multiple jumps.
                    # Recursively call this function, and pass in this direction as the previous jump direction so there is no infinite jump loop.
                    other_jumps = self.get_legal_moves_for_checker(
                        checker_info = {
                            "color" : color,
                            "type" : checker_type,
                            "location" : two_square_info["location"],
                        },
                        all_pieces_info = all_pieces_info,
                        previous_jump_direction = direction,
                    )

                    # Only keep legal actions that have a jump.
                    other_jumps = [j for j in other_jumps if "jumps_over" in j]

                    # If there are no other jumps, then add this move as a jump.
                    print ("Current Scope: Starting location: {loc}".format(loc=start_location)) # TODO
                    print ("How many other jumps are there? {num}".format(num=len(other_jumps))) # TODO

                    initial_jump = {
                        "start": start_location,
                        "jumps_over": [ info["location"] ],
                        "lands" : [ two_square_info["location"] ],
                        "end": two_square_info["location"],
                    }

                    if not other_jumps:
                        legal_moves_with_jumps.append(initial_jump)

                    # For each recursive jump
                    for j in other_jumps:
                        # Combine jumps and landings with this jump.
                        new_multi_jump = {}

                        # Start point is start_location
                        new_multi_jump['start'] = start_location

                        # End point is the end point of the jump
                        new_multi_jump['end'] = j['end']

                        # If there is no jump listing, then create one with the end point
                        if not "jumps_over" in new_multi_jump:
                            new_multi_jump["jumps_over"] = [ info["location"] ]
                            new_multi_jump["lands"] = [ two_square_info["location"] ]

                        # Append new jump onto current list of jumps
                        new_multi_jump["jumps_over"].extend(j["jumps_over"])

                        # Append new landing onto current list of landings
                        new_multi_jump["lands"].extend(j["lands"])

                        # Add new move to list.
                        legal_moves_with_jumps.append(new_multi_jump)

        # If any moves have a jump in it, you must remove all non-jump moves.
        if len(legal_moves_with_jumps) > 0:
            print (legal_moves_with_jumps)
            return legal_moves_with_jumps

        print (legal_moves_without_jumps)
        return legal_moves_without_jumps

# - knows whose turn it is
# - knows who won
# - knows move history
# - knows valid moves
