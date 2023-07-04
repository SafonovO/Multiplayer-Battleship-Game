from normal_ship import NormalShip

ship = NormalShip(4, 1)

size = ship.get_size()
print(size)

print("default vertical. is horisontal?")
print(ship.is_horizontal())
print("toggling. is horizontal?")
ship.toggle_orientation()
print(ship.is_horizontal())

c = (1, 1)

print("testing coord funcitons before setting coords. all should be None")

print(ship.occupies(c))
print(ship.hit(c))
print(ship.check_cell(c))
print(ship.is_sunk())
#ship.toggle_orientation()
#print(ship.is_horizontal())
print(ship.hit_squares())
print(ship.healthy_squares())
print(ship.get_coords())

print("\nsetting coords and testing all coord fucntions. top left at (1, 1)")
print("Is ship currently horizontal?")
print(ship.is_horizontal())
print()

ship.set_coords(c)
ship.print_ship()

print('testing occupies. expecting T,T,F,F')
print(ship.occupies(c))
print(ship.occupies((4, 1)))
print(ship.occupies((1, 2)))
print(ship.occupies((0, 0)))

print("testing hit on cells")
print("ship before:")
ship.print_ship()

print("Hitting (2, 1) and (3, 1) and (7, 1)")
ship.hit((3, 1))
ship.hit((2, 1))
ship.hit((7, 1))
print("Ship after")
ship.print_ship()

print("Checking is sunk. expect false")
print(ship.is_sunk())

print("checking cells. expect T,T,F,F,None")
print(ship.check_cell((1, 1)))
print(ship.check_cell((4, 1)))
print(ship.check_cell((3, 1)))
print(ship.check_cell((2, 1)))
print(ship.check_cell((1, 4)))

print("checking hit squares")
print(ship.hit_squares())

print('checking healthy squares')
print(ship.healthy_squares())


