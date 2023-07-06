from ships.normal_ship import NormalShip
from ships.ship import Ship
from cell import Cell

class BoardFactory:
	# size of board and number of ships
	_size = 0
	_nships = 0

	def __init__(self, size, num_ships):
		self._size = size
		self._nships = num_ships

	# Return a list of nships ships
	def create_ships(self):
		ships = []

		for i in range(self._nships):
			ship = NormalShip(1)
			ships.append(ship)

		return ships

	# create the cells
	def create_cells(self):
		cells = []
		for x in range(self._size):
			row = []
			for y in range(self._size):
				row.append(Cell((x, y)))
			cells.append(row)

		return cells
