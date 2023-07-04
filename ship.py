'''
This class is meant to be an interface. Concrete implementations
of Ships will inherit from this class.

Python does not do interfaces, so every method in this class
will just do nothing.
'''


class Ship:
    # Gets the size of the ship
    def get_size(self):
        pass

    '''
    We need to set the Coords of the ship when we place it on
    the board. This function will do that

    Will take in one Coords as argument: The "tip", which
    represents the coordinates of the top left square.
    '''
    def set_coords(self, tip):
        pass


    # This function checks if this ship occupies a given coord (x, y)
    # return None if coords are not set yet
    def occupies(self, coord):
        pass


    '''
    This function "hits" a square of this ship.
    Assumes the coord is part of the ship. If it isnt,
    just do nothing.
    '''
    def hit(self, coord):
        pass

    '''
    This function tells you if a given cell is healthy of not

    Assumes the cell is part of the ship. If it isnt, return None
    '''
    def check_cell(self, coord):
        pass

    '''
    Returns if this ship is destoryed
    A ship is destroyed if all its squares are hit
    '''
    def is_sunk(self):
        pass

    '''
    Ships can be oriented Horizontally or vertically.
    This method tells us if the ship is horizontal
    '''
    def is_horizontal(self):
        pass

    '''
    Ships can chnage their orientation. This will be implemented
    as a "toggle".
    '''
    def toggle_orientation(self):
        pass


    # Returns a list of all squares on this ship that are hit
    def hit_squares(self):
        pass


    # Returns a list of all squares on this ship that are not hit
    def healthy_squares(self):
        pass


    # Returns a list of all Coords occupied by this ship
    def get_coords(self):
        pass
