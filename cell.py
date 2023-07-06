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

    def __init__(self, coords) -> None:
        self.coordinates = coords

    def set_ship(self, ship: Ship):
        self.ship = ship

    def hit(self) -> bool:
        if self.ship == None:
            return False
        self.is_hit = True
        return True

    def print_cell(self):
        print("Coords:", self.coordinates, "Hit?", self.is_hit)

    def draw_cell(self, x, y, cell_size, screen):
        '''
        x, y are the coordinate of the top left corner
        of the cell.

        cell_size is the side length (pixels) of the cell

        screen is the screen on which we draw
        '''

        cell = pygame.Rect(x, y, cell_size, cell_size)

        pygame.draw.rect(screen, "#59A2E1", cell, 2)


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