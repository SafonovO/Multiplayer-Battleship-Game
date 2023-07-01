from abc import ABC, abstractmethod
from MenuButtons import *

class View(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def display(self, screen):
        pass

    @abstractmethod
    def handle_input(self, event):
        pass

    @abstractmethod
    def update(self):
        pass

"""
Run a loop in the NavigationManager
check for events, if mouse is clicked call handle input in the View
the View will iterate through the collection of options, checking which one
was clicked by position. If is_clicked method returns true, return the button's
View to the current View and then pass it back to the NavigationManager

"""
class MenuView(View):
    def __init__(self):
        super().__init__()
        self.options = [
            NewGameOption((x, y)),
            LoadGameOption((x, y)),
            TutorialOption((x, y)),
            CreditsOption((x, y)),
            QuitOption((x, y)),
        ]

    def display(self, screen):
        pass

    def handle_input(self, event):
        pass

    def update(self):
        pass