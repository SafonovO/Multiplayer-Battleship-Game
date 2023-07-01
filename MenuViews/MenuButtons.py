from abc import ABC, abstractmethod

import pygame
import pygame_gui

from MenuViews import Views

"""
Abstract class to describe the basic menu option(button)
"""


class MenuElement(ABC):
    """
    Constructor method
    """
    position = ()
    text = ''
    view = ''
    def __init__(self, text, view, position, manager):
        self.text = text
        self.position = position
        self.view = view
        self.internalmanager = manager

    """
    Routing action
    """

    @abstractmethod
    def execute_action(self, Container: []):  # return the new view that is related to this button
        pass

    def is_clicked(self) -> bool:
        pass


    def DeactivateView(self):
        for i in self.internalmanager.root_container.elements:
            i.hide()

class NewGameOption(MenuElement):
    def __init__(self, text, view, position, manager):
        super().__init__(text, view, position, manager)
        self.internalbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (120, 40)),
                                                           text=self.text, manager=manager)

    def execute_action(self, Container: []):
        self.DeactivateView()
        Views.ActivateView(Container, self.internalmanager, 'New Game View')


class LoadGameOption(MenuElement):
    def __init__(self, text, view, position, manager):
        super().__init__(text, view, position, manager)
        self.internalbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (120, 40)),
                                                           text=self.text, manager=manager)

    def execute_action(self, Container: []):
        pass


class TutorialOption(MenuElement):
    def __init__(self, text, view, position, manager):
        super().__init__(text, view, position, manager)
        self.internalbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (120, 40)),
                                                           text=self.text, manager=manager)

    def execute_action(self, Container: []):
        pass


class CreditsOption(MenuElement):
    def __init__(self, text, view, position, manager):
        super().__init__(text, view, position, manager)
        self.internalbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (120, 40)),
                                                           text=self.text, manager=manager)

    def execute_action(self, Container: []):
        pass


class QuitOption(MenuElement):
    def __init__(self, text, view, position, manager):
        super().__init__(text, view, position, manager)
        self.internalbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (120, 40)),
                                                           text=self.text, manager=manager)

    def execute_action(self, Container: []):
        pass


class SinglePlayerOption(MenuElement):
    def __init__(self, text, view, position, manager):
        super().__init__(text, view, position, manager)
        self.internalbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (120, 40)),
                                                           text=self.text, manager=manager)

    def execute_action(self, Container: []):
        pass


class CreateGameOption(MenuElement):
    def __init__(self, text, view, position, manager):
        super().__init__(text, view, position, manager)
        self.internalbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (120, 40)),
                                                           text=self.text, manager=manager)

    def execute_action(self, Container: []):
        pass


class JoinGameOption(MenuElement):
    def __init__(self, text, view, position, manager):
        super().__init__(text, view, position, manager)
        self.internalbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (120, 40)),
                                                           text=self.text, manager=manager)

    def execute_action(self, Container: []):
        pass


class BackOption(MenuElement):
    def __init__(self, text, view, position, manager):
        super().__init__(text, view, position, manager)
        self.internalbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (120, 40)),
                                                           text=self.text, manager=manager)

    def execute_action(self, Container: []):
        if self.view == 'New Game View':
            self.DeactivateView()
            Views.ActivateView(Container,self.internalmanager, 'Menu View')
