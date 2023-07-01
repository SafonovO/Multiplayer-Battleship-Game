'''
This class is meant to be an interface. Concrete implementations
of Ships will inherit from this class.

Python does not do interfaces, so every method in this class
will just do nothing.
'''


class Ship:
    '''
    Returns if this ship is destoryed
    A ship is destroyed if all its squares are hit
    '''

    def isSunk(self) -> bool:
        pass

    '''
	Ships can be oriented Horizontally or vertically.
	This method tells us if the ship is horizontal
	'''

    def isHorizontal(self) -> bool:
        pass

    # Returns a list of all squares on this ship that are hit

    def hitSquares(self):
        pass

    # Returns a list of all squares on this ship that are not hit

    def healthySquares(self):
        pass

    # Returns a list of all Coords occupied by this ship

    def getCoords(self):
        pass
