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

	#def draw_board(self, location, size):
