from ships.ship import Ship
from ships.normal_ship import NormalShip
from cell import Cell
from board_factory import BoardFactory
import math

class Board:
	# number of ships on the board
	_nships = 0

	# array of ships on this board
	_ships = []

	# size of this board
	_size = 0

	# array of cells on this board
	_cells = []

	# factory for board setup
	_board_factory = None

	# coordinates where this board should be drawn
	_coordinates = None

	# track the size of the rectangle representing the board
	_width = 0

	'''
	coordinates is a tuple (x, y) that represents the location
	of the board's top left corner when you draw it on the screen

	width is a number that represents the number of pixels in one
	side length of the board
	'''

	def __init__(self, size, num_ships, coords, width):
		self._nships = num_ships
		self._size = size

		self._coordinates = coords
		self._width = width

		self._board_factory = BoardFactory(self._size, self._nships, self._coordinates, self._width)

	def build_board(self):
		self._cells = self._board_factory.create_cells()
		self._ships = self._board_factory.create_ships()

	def get_size(self):
		return self._size

	def get_num_ships(self):
		return self._nships

	# For testing purposes. Print all the cells in the board
	def print_cells(self):
		col = 0
		for column in self._cells:
			print("Column", col)

			for cell in column:
				cell.print_cell()

			col += 1

	def draw_board(self, screen):
		'''
		location is the coordinates of the top left corner

		rect_size is the size of the total square

		We need to evenly divide rect_size into self._size
		equal segments.

		screen is the screen on which we draw


		UPDATE: i am storing this all in a data member so no need
		'''
		# square_size = rect_size / self._size

		'''
		So, now we have the sqaure sizes. We draw them
		in columns

		x_0 and y_0 are the coords of the top left corner
		of the board
		'''
		x_0 = self._coordinates[0]
		y_0 = self._coordinates[1]

		
		for i in range(self._size):
			for j in range(self._size):
				'''
				cell.draw_cell() takes the following arguments:

				x, y are coordinates of the top left corner

				cell_size is the side length of the cell

				screen is the screen on which we want to draw it
				'''
				cell = self._cells[i][j]

				cell.draw_cell(screen)

	def get_active_cell(self, mouse_pos):
		'''
		Given the position of a mouse, find a cell in self._cells
		such that the mouse collides with the cell.

		Returns None if the mouse does not collide with any cell
		'''
		cell_size = self._width / self._size
		row = math.floor((mouse_pos[1] - self._coordinates[1]) / cell_size)
		column = math.floor((mouse_pos[0] - self._coordinates[0]) / cell_size)
		if row < 0 or column < 0 or row >= self._size or column >= self._size:
			return None

		return self._cells[row][column]

