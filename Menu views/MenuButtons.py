from abc import ABC, abstractmethod
from Views import *
"""
Abstract class to describe the basic menu option(button)
"""


class MenuButton(ABC):
    """
    Constructor method
    """

    def __init__(self, text, position):
        self.text = text
        self.position = position

    """
    Routing action
    """

    @abstractmethod
    def execute_action(self)->View: #return the new view that is related to this button
        pass

    def is_clicked(self)-> bool:
        pass

class NewGameOption(MenuButton):
    def __init__(self, position):
        super().__init__("New Game", position)

    def execute_action(self):
        pass


class LoadGameOption(MenuButton):
    def __init__(self, position):
        super().__init__("Load Game", position)

    def execute_action(self):
        pass


class TutorialOption(MenuButton):
    def __init__(self, position):
        super().__init__("Tutorial", position)

    def execute_action(self):
        pass


class CreditsOption(MenuButton):
    def __init__(self, position):
        super().__init__("Credits", position)

    def execute_action(self):
        pass


class QuitOption(MenuButton):
    def __init__(self, position):
        super().__init__("Quit", position)

    def execute_action(self):
        pass


class SinglePlayerOption(MenuButton):
    def __init__(self, position):
        super().__init__("Play vs AI", position)

    def execute_action(self):
        pass


class CreateGameOption(MenuButton):
    def __init__(self, position):
        super().__init__("Create Game", position)

    def execute_action(self):
        pass


class JoinGameOption(MenuButton):
    def __init__(self, position):
        super().__init__("Join Game", position)

    def execute_action(self):
        pass


class BackOption(MenuButton):
    def __init__(self, position):
        super().__init__("Join Game", position)

    def execute_action(self):
        pass
