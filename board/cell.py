import pygame

from utilities.fonts import get_font
# import pygame_gui
# from menu_views.menu_options import MenuElement
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
    __is_guessed: bool = False

    # for drawing purposes. the side length and location of the cell
    __width = 0
    __location = None
    __bigMarkingSize = 36
    __smallMarkingSize = 24
    '''
    width represents a number of pixels that is the side length
    of the cell when you draw it on the screen

    location is a tuple (x, y) that represents the coordinates of
    the top left corner of the cell when it is drawn on teh screen
    '''

    def __init__(self, coords, width, location) -> None:
        self.coordinates = coords
        self.__width = width
        self.__location = location

    def set_ship(self, ship: Ship):
        self.ship = ship

    def set_is_guessed(self, bool):
        self.__is_guessed = bool

    def get_is_guessed(self):
        return self.__is_guessed

    def hit(self) -> bool:
        self.is_hit = True

        if self.ship == None:
            return False

        self.ship.hit()

        return True

    def print_cell(self):
        print("Coords:", self.coordinates, "Hit?", self.is_hit, "Ship?", self.ship != None)


    def draw_cell(self, screen, display):
        '''
        x, y are the coordinate of the top left corner
        of the cell.

        self_width is the side length (pixels) of the cell

        screen is the screen on which we draw

        display indicates if we should draw unhit
        ship cells differently. This would be done
        on my board only, not the opponenets board
        '''
        markingSize = self.__smallMarkingSize if display else self.__bigMarkingSize

        x = self.__location[0]
        y = self.__location[1]

        cell = pygame.Rect(x, y, self.__width, self.__width)

        # Get the center of the cell
        cell_center = self.get_cell_center()

        # If cell is a hit ship, print an X on it
        x_text = get_font(markingSize, "Helvetica").render("X", True, "White")
        x_rect = x_text.get_rect(center=cell_center)

        # if cell missed, print a - on it
        dash_text = get_font(markingSize, "Helvetica").render("-", True, "Black")
        dash_rect = dash_text.get_rect(center=cell_center)

        # if display, draw unhit ships differently
        if display and self.ship != None and self.is_hit == False:
            pygame.draw.rect(screen, "Grey", cell)
            ship = pygame.image.load("assets/ship.png")
            ship = pygame.Surface.convert_alpha(ship)
            ship = pygame.transform.scale(ship, (self.__width, self.__width))
            screen.blit(ship, self.get_cell_corner())

        # draw a cell that has not been fired on
        elif not self.is_hit:
            pygame.draw.rect(screen, "#59A2E1", cell, 2)

        # draw a cell that has been fired on with no ship
        elif self.is_hit and self.ship == None:
            # draw the square yellow
            pygame.draw.rect(screen, "#DAE159", cell)
            # draw the dash
            screen.blit(dash_text, dash_rect)

        # draw a cell that has been fired on with ship
        elif self.is_hit and self.ship != None:
            pygame.draw.rect(screen, "Red", cell)
            # draw the X
            screen.blit(x_text, x_rect)


    def draw_selected_cell(self, screen):
        # Draw a special cell that has been selected
        x = self.__location[0]
        y = self.__location[1]

        cell = pygame.Rect(x, y, self.__width, self.__width)

        # Get the center of the cell
        cell_center = self.get_cell_center()

        # Draw teh cell in green
        pygame.draw.rect(screen, "Green", cell)

        # Draw its marking
        question_text = get_font(self.__bigMarkingSize, "Helvetica").render("?", True, "Black")
        question_rect = question_text.get_rect(center=cell_center)
        screen.blit(question_text, question_rect)


    def get_cell_center(self):
        return (self.__location[0] + (0.5*self.__width), self.__location[1] + (0.5*self.__width))

    def get_cell_corner(self):
        return (self.__location[0], self.__location[1])

    def get_width(self):
        return self.__width


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