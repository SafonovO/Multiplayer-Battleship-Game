import pygame
import pygame_gui
from pygame_gui.core import ObjectID


class Rectangle:
    position = ()
    view = ''


    def __init__(self, view, position,dimensions, styleId ,manager):
        self.position = position
        self.view = view
        self.internalmanager = manager
        self.internalelement = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect(position, dimensions), starting_height=0, manager=manager, object_id=ObjectID(class_id=styleId))
