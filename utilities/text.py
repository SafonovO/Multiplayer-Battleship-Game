import pygame
import pygame_gui
from pygame_gui.core import ObjectID


class Label:
    position = ()
    view = ''

    def __init__(self, text, view, position, dimensions, styleId, manager):
        self.position = position
        self.view = view
        self.internalmanager = manager
        self.internalelement = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect(position, dimensions),
                                                             manager=manager,
                                                             object_id=ObjectID(class_id=styleId), html_text=text)
