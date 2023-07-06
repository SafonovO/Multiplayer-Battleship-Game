import pygame
#import pygame_gui
#from menu_views.menu_options import MenuElement
from ships.normal_ship import Ship

'''

class Button:
    position = (0, 0)
    text = ''
    manager = None
    gui_button = None

    def __init__(self, position: tuple, text: str, manager: pygame_gui.UIManager, height: int, width: int):
        self.position = position
        self.text = text
        self.manager = manager
        self.gui_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(
            position, (width, height)), manager=manager)
        
    def on_click(self):
        pass
'''

class Cell:
    coordinates = (0, 0)
    ship: Ship = None
    is_hit: bool = False

    # for drawing purposes. the side length and location of the cell
    _width = 0
    _location = None

    def __init__(self, coords, width, location) -> None:
        self.coordinates = coords
        self._width = width
        self._location = location

    def set_ship(self, ship: Ship):
        self.ship = ship

    def hit(self) -> bool:
        if self.ship == None:
            return False
        self.is_hit = True
        return True

    def print_cell(self):
        print("Coords:", self.coordinates, "Hit?", self.is_hit)

    def draw_cell(self, screen):
        '''
        x, y are the coordinate of the top left corner
        of the cell.

        self_width is the side length (pixels) of the cell

        screen is the screen on which we draw
        '''

        x = self._location[0]
        y = self._location[1]

        cell = pygame.Rect(x, y, self._width, self._width)

        # draw a cell that has not been fired on
        if self.is_hit == False:
            pygame.draw.rect(screen, "#59A2E1", cell, 2)

        # draw a cell that has been fired on
        else:
            pygame.draw.rect(screen, "Red", cell)


'''
class UICell(Button):
    cell = None
    def __init__(self, position: tuple, text: str, manager: pygame_gui.UIManager, size: int, coordinates: tuple):
        super().__init__(position, text, manager, height=size, width=size)
        self.cell = Cell(coordinates)
        self.gui_button.show()

    def on_click(self):
        pass

'''