import pygame

from ui.fonts import get_font
from ships.normal_ship import Ship

ship_1x1 = pygame.image.load("assets/ships/ship_1x1.png")
ship_head = pygame.image.load("assets/ships/ship_head.png")
ship_middle = pygame.image.load("assets/ships/ship_middle.png")
ship_tail = pygame.image.load("assets/ships/ship_tail.png")


class Cell:
    coordinates: tuple[int, int] = (0, 0)
    ship: Ship | None = None
    is_guessed: bool = False
    is_hit: bool = False
    foreign: bool = False
    index: int = -1

    # for drawing purposes. the side length and location of the cell
    __width = 0
    __location = None
    __bigMarkingSize = 36
    __smallMarkingSize = 24
    """
    width represents a number of pixels that is the side length
    of the cell when you draw it on the screen

    location is a tuple (x, y) that represents the coordinates of
    the top left corner of the cell when it is drawn on teh screen
    """

    def __init__(self, coords, width, location, foreign=False) -> None:
        self.coordinates = coords
        self.foreign = foreign
        self.__width = width
        self.__location = location

    def set_ship(self, ship: Ship):
        self.ship = ship

    def set_index(self, index: int):
        self.index = index

    def hit(self) -> bool:
        self.is_guessed = True

        if self.ship == None:
            return False

        self.is_hit = True
        self.ship.hit()

        return True

    def multiplayer_hit(self, hit: bool):
        self.is_guessed = True
        self.is_hit = hit

    def print_cell(self):
        print("Coords:", self.coordinates, "Hit?", self.is_hit, "Ship?", self.ship != None)

    def draw_cell(self, screen: pygame.Surface, display):
        """
        x, y are the coordinate of the top left corner
        of the cell.

        self_width is the side length (pixels) of the cell

        screen is the screen on which we draw

        display indicates if we should draw unhit
        ship cells differently. This would be done
        on my board only, not the opponenets board
        """
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
        if display and self.ship is not None and self.is_hit == False:
            if self.ship.get_size() == 1:
                ship = ship_1x1
            elif self.index == 0:
                ship = ship_head
            elif self.index == self.ship.get_size() - 1:
                ship = ship_tail
            else:
                ship = ship_middle
            ship = pygame.Surface.convert_alpha(ship)
            ship = pygame.transform.scale(ship, (self.__width, self.__width))
            if not self.ship.vertical:
                ship = pygame.transform.rotate(ship, 90)
            screen.blit(ship, self.get_cell_corner())

        # draw a cell that has not been fired on
        elif not self.is_guessed:
            pygame.draw.rect(screen, "#59A2E1", cell, 2)

        # draw a cell that has been fired on without hitting a ship
        elif not self.is_hit:
            # draw the square yellow
            pygame.draw.rect(screen, "#DAE159", cell)
            # draw the dash
            screen.blit(dash_text, dash_rect)

        # draw a cell that has been fired on hitting a ship
        else:
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

    def draw_cell_color(self, screen, color):
        # Draw this cell on the specified screen in the specifed color
        # Draw a special cell that has been selected
        x = self.__location[0]
        y = self.__location[1]

        cell = pygame.Rect(x, y, self.__width, self.__width)

        # Get the center of the cell
        cell_center = self.get_cell_center()

        # Draw teh cell in green
        pygame.draw.rect(screen, color, cell)

    def get_cell_center(self):
        return (
            self.__location[0] + (0.5 * self.__width),
            self.__location[1] + (0.5 * self.__width),
        )

    def get_cell_corner(self):
        return (self.__location[0], self.__location[1])

    def get_width(self):
        return self.__width
