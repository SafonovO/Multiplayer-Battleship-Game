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
back_button_image = pygame.image.load("assets/back_arrow.png")
hovered_back = pygame.image.load("assets/back_arrow_hover.png")
volume_image = pygame.image.load("assets/volume.png")
hovered_volume = pygame.image.load("assets/volume_hover.png")
plus_button_image = pygame.image.load("assets/plus.png")
minus_button_image = pygame.image.load("assets/minus.png")
help_button_image = pygame.image.load("assets/help.png")
help_button_hover = pygame.image.load("assets/help_hover.png")
small_x_image = pygame.image.load("assets/x_small.png")
small_dash_image = pygame.image.load("assets/dash_small.png")

def make_button(x, y, text, font_size, reactive=False, image=base_button_image,
                hovered_image=hovered_button_image):
    button = Button(image=image, pos=(x, y))
    if reactive:
        button = ReactiveButton(
            button,
            hover_surface=hovered_image,
            active_surface=hovered_image,
        )
    return TextButton(button, text=text, font=get_font(font_size))

def make_back_button():
    return make_button(175, 115, "", 75, reactive=True, image=back_button_image, 
                       hovered_image=hovered_back)

def make_volume_button():
    return make_button(1250, 40, "", 0, reactive=True, image=volume_image, hovered_image=hovered_volume)

def make_help_button():
    return make_button(1250, 125, "", 0, reactive=True, image=help_button_image, hovered_image=help_button_hover)