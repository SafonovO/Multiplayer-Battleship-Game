import pygame

class NavigationManager:
    def __init__(self):
        self.view_stack = []
        self.switch_to_view(initial_view)


    def handle_input(self, event):
        if self.view_stack:
            self.view_stack[-1].handle_input(event)

    def update(self):
        if self.view_stack:
            self.view_stack[-1].update()

    def switch_to_view(self, new_view):
        self.view_stack.append(new_view)

    def switch_to_previous_view(self):
        if len(self.view_stack) > 1:
            self.view_stack.pop()

    def display_views(self, screen):
        for view in self.view_stack:
            view.display(screen)