import pygame
from pygame.locals import *
from ui.button import Button, ReactiveButton, TextButton
from ui.fonts import get_font

base_button_image = pygame.image.load("assets/navy_button.png")
hovered_button_image = pygame.image.load("assets/navy_button_hover.png")
quit_button_image = pygame.image.load("assets/quit.png")
confirm_button_image = pygame.image.load("assets/ConfirmButton.png")
confirm_button_greyed = pygame.image.load("assets/ConfirmButtonGreyed.png")
confirm_button_select = pygame.image.load("assets/ConfirmSelected.png")


def make_button(x, y, text, font_size, reactive=False, image=base_button_image):
    button = Button(image=image, pos=(x, y))
    if reactive:
        button = ReactiveButton(
            button,
            hover_surface=hovered_button_image,
            active_surface=hovered_button_image,
        )
    return TextButton(button, text=text, font=get_font(font_size))
