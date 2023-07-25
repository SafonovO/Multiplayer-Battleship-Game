from board.cell import Cell
from ships.normal_ship import NormalShip


class BoardFactory:
    # size of board and number of ships
    __size = 0
    __nships = 0
    __coords = None
    __width = 0

    def __init__(self, size, num_ships, coords, width):
        self.__size = size
        self.__nships = num_ships
        self.__coords = coords
        self.__width = width

    # Return a list of nships ships
    def create_ships(self):
        ships = []

        for i in range(self.__nships):
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
        cell_size = self.__width / self.__size
        x_0 = self.__coords[0]
        y_0 = self.__coords[1]

        cells = []
        for x in range(self.__size):
            row = []
            for y in range(self.__size):
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
