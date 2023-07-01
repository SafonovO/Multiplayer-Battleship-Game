'''
Class to represent a pair of (x, y) coordinates
on the Battleship board.
'''


class Coords:
    '''
    x and y are private variables, indicated by the
    underscore preceeding their name.

    By default, they are None, and are set in the constructor

    After construction, they should not be able to be changed.
    So this class will not have a setter.
    '''
    _x = None
    _y = None

    def __init__(self, x, y):
        # Constructor, set x and y coordinates
        self._x = x
        self._y = y

    # Returns the x and y values in a tuple
    def get_coords(self) -> tuple:
        return (self._x, self._y)

    # Tells us if this is a valid Coord (ie. not None)
    def valid(self) -> bool:
        return self._x is not None and self._y is not None
