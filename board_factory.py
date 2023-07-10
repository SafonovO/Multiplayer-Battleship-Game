from cell import Cell
from ships.normal_ship import NormalShip


class BoardFactory:
    # size of board and number of ships
    _size = 0
    _nships = 0
    _coords = None
    _width = 0

    def __init__(self, size, num_ships, coords, width):
        self._size = size
        self._nships = num_ships
        self._coords = coords
        self._width = width

    # Return a list of nships ships
    def create_ships(self):
        ships = []

        for i in range(self._nships):
            ship = NormalShip(1)
            ships.append(ship)

        return ships

    # create the cells
    def create_cells(self):
        '''
        cell size is the total width of the board (_width)
        divided by the number of cells (_size)

        x_0 and y_0 are the coordinates of teh baord
        '''
        cell_size = self._width / self._size
        x_0 = self._coords[0]
        y_0 = self._coords[1]

        cells = []
        for x in range(self._size):
            row = []
            for y in range(self._size):
                '''
                Cell contructor requires an (x, y), width, and
                location.

                x, y are the coordinates of teh cell relative to the board

                width is the side length in pixels of the cell when we draw it

                location is the coordinates of the top left corner of the
                cell when we draw it
                '''

                location_x = x_0 + x * cell_size
                location_y = y_0 + y * cell_size

                row.append(Cell(coords=(x, y), width=cell_size, location=(location_x, location_y)))
            cells.append(row)

        return cells
