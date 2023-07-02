
import pygame
import pygame_gui
from pygame_gui.core import ObjectID

from MenuViews import Views

"""
Abstract class to describe the basic menu option(button)
"""


class MenuElement:
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


    def execute_action(self, routingStack, container: []):  # return the new view that is related to this button
        pass

    def deactivateView(self):
        for i in self.internalmanager.root_container.elements:
            i.hide()


class NewGameOption(MenuElement):
    def __init__(self, text, view, position, manager):
        super().__init__(text, view, position, manager)
        self.internalbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (120, 40)),
                                                           text=self.text, manager=manager)
    def execute_action(self, routingStack, container: []):
        self.deactivateView()
        Views.ActivateView(routingStack, container, self.internalmanager, 'New Game View', False)


class LoadGameOption(MenuElement): #TODO implement
    def __init__(self, text, view, position, manager):
        super().__init__(text, view, position, manager)
        self.internalbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (120, 40)),
                                                           text=self.text, manager=manager)
    def execute_action(self, RoutingStack, Container: []):
        self.deactivateView()
        Views.ActivateView(RoutingStack, Container, self.internalmanager, 'Load Game View', False)


class TutorialOption(MenuElement):#TODO implement
    def __init__(self, text, view, position, manager):
        super().__init__(text, view, position, manager)
        self.internalbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (120, 40)),
                                                           text=self.text, manager=manager)
    def execute_action(self, routingStack, container: []):
        self.deactivateView()
        Views.ActivateView(routingStack, container, self.internalmanager, 'Tutorial View', False)


class CreditsOption(MenuElement):#TODO implement
    def __init__(self, text, view, position, manager):
        super().__init__(text, view, position, manager)
        self.internalbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (120, 40)),
                                                           text=self.text, manager=manager)
    def execute_action(self, routingStack, container: []):
        pass


class QuitOption(MenuElement):#TODO implement
    def __init__(self, text, view, position, manager):
        super().__init__(text, view, position, manager)
        self.internalbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (120, 40)),
                                                           text=self.text, manager=manager,object_id=ObjectID(class_id = '@quit_button'))
    def execute_action(self, rutingStack, container: []):
        pygame.quit()


class SinglePlayerOption(MenuElement):#TODO implement
    def __init__(self, text, view, position, manager):
        super().__init__(text, view, position, manager)
        self.internalbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (120, 40)),
                                                           text=self.text, manager=manager)
    def execute_action(self, routingStack, container: []):
        pass


class CreateGameOption(MenuElement):#TODO implement
    def __init__(self, text, view, position, manager):
        super().__init__(text, view, position, manager)
        self.internalbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (120, 40)),
                                                           text=self.text, manager=manager)
    def execute_action(self, routingStack, container: []):
        pass


class JoinGameOption(MenuElement):#TODO implement
    def __init__(self, text, view, position, manager):
        super().__init__(text, view, position, manager)
        self.internalbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (120, 40)),
                                                           text=self.text, manager=manager)
    def execute_action(self, routingStack, container: []):
        pass


class BackOption(MenuElement):
    def __init__(self, text, view, position, manager):
        super().__init__(text, view, position, manager)
        self.internalbutton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (120, 40)),
                                                           text=self.text, manager=manager)
    def execute_action(self, routingStack, container: []):
        routingStack.pop()
        self.deactivateView()
        Views.ActivateView(routingStack, container, self.internalmanager, routingStack[-1], True)
