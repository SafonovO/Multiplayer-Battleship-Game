from ships.ship import Ship
from ships.normal_ship import NormalShip
from cell import Cell
from board_factory import BoardFactory
import pygame

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

	def __init__(self, size, num_ships):
		self._nships = num_ships
		self._size = size

		self._board_factory = BoardFactory(self._size, self._nships)

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

	def draw_board(self, location, rect_size, screen):
		'''
		location is the coordinates of the top left corner

		rect_size is the size of the total square

		We need to evenly divide rect_size into self._size
		equal segments.

		screen is the screen on which we draw
		'''
		square_size = rect_size / self._size

		'''
		So, now we have the sqaure sizes. We draw them
		in columns

		x_0 and y_0 are the coords of the top left corner
		of the board
		'''
		x_0 = location[0]
		y_0 = location[1]

		
		for i in range(self._size):
			for j in range(self._size):
				'''
				cell.draw_cell() takes the following arguments:

				x, y are coordinates of the top left corner

				cell_size is the side length of the cell

				screen is the screen on which we want to draw it
				'''
				cell = self._cells[i][j]
				x = x_0 + i*square_size
				y = y_0 + j*square_size

				cell.draw_cell(x, y, square_size, screen)


