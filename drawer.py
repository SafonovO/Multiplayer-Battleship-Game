import pygame
from pygame.locals import *
from pygame import mixer
from utilities.button import Button,ReactiveButton, TextButton
from utilities.fonts import get_font
from utilities.input import Input
from enum import Enum


pygame.init()
pygame.display.set_caption("Battleship")
base_button_image = pygame.image.load("assets/navy_button.png")
hovered_button_image = pygame.image.load("assets/navy_button_hover.png")
quit_button_image = pygame.image.load("assets/quit.png")
confirm_button_image = pygame.image.load("assets/ConfirmButton.png")
PLAYING_SURFACE = pygame.Rect(100, 50, 1100, 700)

SCREEN = pygame.display.set_mode((1300, 800))
BG = pygame.image.load("assets/Background.png")

button_array =[]
text_array=[]

class Element(Enum):
    QUIT_BUTTON=0
    PLAY_BUTTON=1
    JOIN_BUTTON=1
    EASY_BUTTON=1
    ROTATE_BUTTON=1
    FIRE_BUTTON=1
    AI_PLAY_BUTTON=2
    CONFIRM_BUTTON=2
    CREATE_BUTTON=2
    HARD_BUTTON=2
    
def make_button(x, y, text, font_size, reactive=False, image=base_button_image):
        button = Button(image=image, pos=(x, y))
        if reactive:
            button = ReactiveButton(
                button,
                hover_surface=hovered_button_image,
                active_surface=hovered_button_image,
            )
        return TextButton(button, text=text, font=get_font(font_size))

def make_text(text: str, pos: tuple[int, int], size: int, colour: str):
    text_rendered = get_font(size).render(text, True, colour)
    text_rect = text_rendered.get_rect(center=pos)
    return (text_rendered, text_rect)
    
class Drawer():
    def __init__(self):
        pass
    
    coord_tuple=None
    
    def draw_screen(self,screen,ships_left=None, manager=None, input_code=""):
        if(screen=='main'):
            self.main_menu()
        elif(screen=='select_opponent'):
            self.select_op()
        elif(screen=='human_settings'):
            self.human_settings()
        elif screen== "human_create_pending":
            self.human_create_pending(manager)
        elif(screen=='AI_settings'):
            self.ai()
        elif(screen=='placement'):
            self.placement(ships_left)
        elif(screen=='play'):
            self.play()
    
    def main_menu(self):
        text = get_font(100).render("BATTLESHIP", True, "#b68f40")
        text_rect = text.get_rect(center=(650, 150))
        text_tuple=(text, text_rect)
        play_button = make_button(650, 350, "PLAY", 75, reactive=True)
        quit_button = make_button(650, 550, "QUIT", 75, reactive=True)
        
        for button in [quit_button,play_button]:
            button_array.append(button)
        
        for tuple in [text_tuple]:
            text_array.append(tuple)
        
    def select_op(self):
        play_button_ai = make_button(650, 150, "Play vs. AI", 50, reactive=True)
        play_button_human = make_button(650, 350, "Play vs. Human", 50, reactive=True)
        quit_button = make_button(650, 550, "QUIT", 75, reactive=True)
        
        for button in [quit_button,play_button_human,play_button_ai]:
            button_array.append(button)
    
    def human_settings(self):
        create_button = make_button(650, 150, "Create Game", 50, reactive=True)
        join_button = make_button(650, 350, "Join Game", 50, reactive=True)
        quit_button = make_button(650, 550, "QUIT", 75, reactive=True)
        
        for button in [quit_button,join_button,create_button]:
            button_array.append(button)
    
    def human_create_pending(self, manager):
        quit_button = make_button(1000, 25, "QUIT", 20, image=quit_button_image)

        waiting_title = make_text("Waiting for opponent", (650, 300), 50, "#b68f40")
        waiting_text = make_text(
            "You can invite a friend to this game with the code below",
            (650, 375),
            30,
            "#ffffff"
        )

        code = get_font(30).render(manager.client.code, True, "#b68f40")
        code_rect = code.get_rect(center=(650, 425))
        code_tuple = (code, code_rect)
            
        for tuple in [waiting_title, waiting_text, code_tuple]:
            text_array.append(tuple)

        for button in [quit_button]:
            button_array.append(button)

    def human_join(self, code_input: Input, manager):
        quit_button = make_button(1000, 25, "QUIT", 20, image=quit_button_image)

        join_title = make_text("Join game", (650, 300), 50, "#b68f40")
        join_desc = make_text("Enter an invite code to join a game", (650, 375), 30, "#ffffff")
        
        code_chars = make_text(" ".join(code_input.value.ljust(9, "_")), (650, 425), 30, "#b68f40")

        join_button = make_button(650, 550, "Join", 50, reactive=True)
            
        for tuple in [join_title, join_desc, code_chars]:
            text_array.append(tuple)

        for button in [quit_button, join_button]:
            button_array.append(button)
        pass
            
    def ai(self):
        text = get_font(50).render("Difficulty", True, "#b68f40")
        text_rect = text.get_rect(center=(650, 100))
        text_tuple=(text,text_rect)
        quit_button = make_button(650, 550, "QUIT", 75, reactive=True)
        easy_button = make_button(400, 175, "Easy", 20, image=confirm_button_image)
        hard_button = make_button(900, 175, "Hard", 20, image=confirm_button_image)
        
        for button in [quit_button, easy_button, hard_button]:
            button_array.append(button)
            
        for tuple in [text_tuple]:
            text_array.append(tuple)
    
    def placement(self,ships_left):
        # setup labels for the boards
        placement_board_label = get_font(30).render("Board Setup", True, "White")
        placement_board_label_rect = placement_board_label.get_rect(center=(425, 100))
        placement_tuple=(placement_board_label, placement_board_label_rect)
        confirm_button = make_button(1000, 225, "Place", 20, image=confirm_button_image)
        quit_button = make_button(1000, 25, "QUIT", 20, image=quit_button_image)
        rotate_button = make_button(1000, 150, "Rotate", 20, image=confirm_button_image)

        ships_left_label = get_font(30).render("Ships Left: " + str(ships_left), True, "White")
        ships_left_label_rect = ships_left_label.get_rect(center=(1000, 100))
        ships_left_tuple=(ships_left_label, ships_left_label_rect)
        for tuple in [placement_tuple, ships_left_tuple]:
            text_array.append(tuple)
            
        for button in [quit_button,rotate_button,confirm_button]:
            button_array.append(button)
    
    def play(self):
        # setup labels for the boards
        opponent_board_label = get_font(30).render("OPPONENT'S BOARD", True, "White")
        opponent_board_label_rect = opponent_board_label.get_rect(center=(425, 100))
        opponent_tuple=(opponent_board_label,opponent_board_label_rect)

        my_board_label = get_font(30).render("MY BOARD", True, "White")
        my_board_label_rect = my_board_label.get_rect(center=(1000, 325))
        my_board_tuple=(my_board_label,my_board_label_rect)
        
        fire_button = make_button(1000, 250, "FIRE", 20, image=confirm_button_image)
        quit_button = make_button(1000, 25, "QUIT", 20, image=quit_button_image)

        # Create text
        select_text = get_font(15).render("YOU HAVE SELECTED:", True, "White")
        select_text_rect = select_text.get_rect(center=(1000, 150))
        select_tuple=(select_text,select_text_rect)
        
        for tuple in [opponent_tuple,my_board_tuple,select_tuple]:
            text_array.append(tuple)
            
        for button in [quit_button,fire_button]:
            button_array.append(button)
            
    def render_screen(self,mouse,playing_surface=False):
        SCREEN.blit(BG, (0, 0))
        if (playing_surface):
            pygame.draw.rect(SCREEN, "#042574", PLAYING_SURFACE)
        if (self.coord_tuple!=None):
            SCREEN.blit(self.coord_tuple[0],self.coord_tuple[1])
        for element in text_array:
            SCREEN.blit(element[0], element[1])
        for button in button_array:
            button.render(SCREEN, mouse)
            
    def draw_coord(self,num, letter):
        coord_text = get_font(15).render("({}, {})".format(letter, num), True, "White")
        coord_text_rect = coord_text.get_rect(center=(1000, 200))
        self.coord_tuple=(coord_text,coord_text_rect)

    def clear_coord(self):
        self.coord_tuple=None

    def clear_array(self):
        button_array.clear()
        text_array.clear()