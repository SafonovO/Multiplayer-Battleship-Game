from ship import Ship

class NormalShip(Ship):
	# These store the length and width of the ship
	# They are pruvate and cannot be changed (no setter)
	_length = None
	_width = None

	'''
	coords will be a dictionary whose keys will be the Coords
	occupied by the ship.

	coords[(x, y)] will map to a boolean value that indicates
	if that coordinate has been hit or not.

	coords[(x, y)] == True means that coordinate is healthy
	'''
	_coords = None

	# Tracks if the ship is Horizontal or Vertical
	# Ships are vertical by default
	_isHorizontal = False

	# Constructor: sets length and width
	def __init__(self, length, width):
		self._length = length
		self._width = width

	# length and width getter
	def get_size(self):
		# return in dict form
		return {"length": self._length, "width": self._width}
	'''
	We need to set the Coords of the ship when we place it on
	the board. This function will do that

	Will take in one Coords as argument: The "tip", which
	represents the coordinates of the top left square.

	Also, when we set, we set all the squares to be healthy
	'''
	def set_coords(self, tip):
		# coords of the tip are x_0, y_0
		x_0 = tip[0]
		y_0 = tip[1]

		self._coords = {}

		'''
		By default, ships are vertical. The length and width
		attributes are from the perspective of a vertical ship.

		For example,
		x
		x
		x
		x

		This ship would have a length of 4 and a width of 1

		The same ship oriented horizontally would still 
		have a length of 4 and a width of 1
		'''
		if not self._isHorizontal:
			for x in range(self._width):
				for y in range(self._length):
					newcoord = (x_0 + x, y_0 + y)
					self._coords.update({newcoord: True})

		else:
			for x in range(self._length):
				for y in range(self._width):
					newcoord = (x_0 + x, y_0 + y)
					self._coords.update({newcoord: True})


	# This function checks if this ship occupies a given coord (x, y)
	def occupies(self, coord):
		# Return None if coords ave not been set yet
		if self._coords == None:
			return None

		coords_list = self.get_coords()

		return coord in coords_list


	'''
	This function "hits" a square of this ship.
	Assumes the coord is part of the ship. If it isnt,
	just do nothing.
	'''
	def hit(self, coord):
		# Return immediately if coords are not set
		if self._coords == None:
			return None

		if self.occupies(coord):
			self._coords[coord] = False

	'''
	This function tells you if a given cell is healthy of not

	Assumes the cell is part of the ship. If it isnt, return None
	'''
	def check_cell(self, coord):
		# return immediately if coords are not set
		if self._coords == None:
			return None

		if self.occupies(coord):
			return self._coords[coord]

		else:
			return None

	'''
	Returns if this ship is destoryed
	A ship is destroyed if all its squares are hit
	'''
	def is_sunk(self):
		# return immediately if coords are not set
		if self._coords == None:
			return None

		for coord in self._coords:
			# If any square is healthy, ship is not sunk
			if self._coords[coord] == True:
				return False

		# If no square is healthy, ship is sunk
		return True

	'''
	Ships can be oriented Horizontally or vertically.
	This method tells us if the ship is horizontal
	'''
	def is_horizontal(self):
		return self._isHorizontal

	'''
	Ships can chnage their orientation. This will be implemented
	as a "toggle"
	'''
	def toggle_orientation(self):
		self._isHorizontal = not self._isHorizontal


	# Returns a list of all squares on this ship that are hit
	def hit_squares(self):
		# return immediately if coords are not set
		if self._coords == None:
			return None

		hit_squares = []

		# a square is hit if it maps to F in _coords
		for c in self._coords:
			if self._coords[c] == False:
				hit_squares.append(c)

		return hit_squares


	# Returns a list of all squares on this ship that are not hit
	def healthy_squares(self):
		# return immediately if coords are not set
		if self._coords == None:
			return None

		healthy_squares = []

		for c in self._coords:
			if self._coords[c] == True:
				healthy_squares.append(c)

		return healthy_squares


	# Returns a list of all Coords occupied by this ship
	def get_coords(self):
		# return none if coords are not set
		if self._coords == None:
			return None

		return list(self._coords.keys())

	def print_ship(self):
		# For reference, prints all the coords occupied by this ship
		if self._coords == None:
			return None

		for item in self._coords:
			print(item, ":", self._coords[item])

