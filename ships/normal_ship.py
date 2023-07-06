from .ship import Ship

class NormalShip(Ship):
	# track the size
	_size = None

	# track the HP
	_hp = None

	def __init__(self, ship_size):
		self._size = ship_size
		self._hp = ship_size

	def get_size(self):
		return self._size

	def get_hp(self):
		return self._hp

	'''
	"Hits" this ship.

	Returns a boolean value: True indicates the
	hit resulted in the ship sinking
	'''
	def hit(self):
		# Do not hit a dead ship
		if self._hp <= 0:
			return None

		self._hp -= 1

		# return true if ship has sunk
		return self._hp == 0

	# determine if this ship is sunk
	def sunk(self):
		return self._hp <= 0


'''
# TESTING CODE:

ship = NormalShip(4)
print("Showing size, HP. expect 4 4")
print(ship.get_size())
print(ship.get_hp())
print("Sunk?", ship.sunk())

print("\nHitting twice. expect F F 4 2")
print(ship.hit())
print(ship.hit())
print(ship.get_size())
print(ship.get_hp())
print("Sunk?", ship.sunk())

print("\nHitting twice. expect F T 4 ")
print(ship.hit())
print(ship.hit())
print(ship.get_size())
print(ship.get_hp())
print("Sunk?", ship.sunk())
'''