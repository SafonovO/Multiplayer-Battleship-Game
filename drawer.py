import pygame
import sys
import asyncio
from utilities.button import Button, ReactiveButton, TextButton
from utilities.fonts import get_font
from board.board import Board
from board.cell import Cell

BG = pygame.image.load("assets/Background.png")
base_button_image = pygame.image.load("assets/navy_button.png")
hovered_button_image = pygame.image.load("assets/navy_button_hover.png")
SCREEN = pygame.display.set_mode((1300, 800))


class Drawer:
    pygame.init()
    active_cell=None
    __button_array=[]
    __rect_array=[]
    __coord_text=None
    __coord_text_rect=None
    
    __playing_surface = pygame.Rect(100, 50, 1100, 700)

    ships_left=None
    vertical =True
    
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Drawer, cls).__new__(cls)
        return cls.instance
    
    def render_elements(self, bool, __player1, __player2, place):
        SCREEN.blit(BG, (0, 0))
        mouse = pygame.mouse.get_pos()
        #if true draw the playing area
        if(place):
            #draw playing surface
            pygame.draw.rect(SCREEN, "#042574", self.__playing_surface)
            # Draw the labels
            if(bool):
                
                # draw the coord text if it is not None
                if self.__coord_text != None and self.__coord_text_rect != None:
                    SCREEN.blit(self.__coord_text, self.__coord_text_rect)
                # Draw active cell if it is not None
                if self.active_cell != None:
                    self.active_cell.draw_selected_cell(SCREEN)
                #drawing boards 
                for player in [__player1, __player2]:
                    player.board.draw_board(SCREEN)
                # draw the coord text if it is not None
                if self.active_cell != None:
                    cell_coords = self.active_cell.coordinates
                    letter = Board.letters[cell_coords[0]]
                    num = cell_coords[1] + 1
                    self.__coord_text = get_font(15).render("({}, {})".format(letter, num), True, "White")
                    self.__coord_text_rect = self.__coord_text.get_rect(center=(1000, 200))
            else:
                ships_left_label = get_font(30).render("Ships Left: " + str(self.ships_left), True, "White")
                ships_left_label_rect = ships_left_label.get_rect(center=(1000, 100))
                SCREEN.blit(ships_left_label,ships_left_label_rect)
                __player1.draw_large_board(SCREEN)
                if self.active_cell is not None:
                    self.active_cell.draw_selected_cell(SCREEN)
            
        #draw buttons
        
        
        for i in range(0, len(self.__rect_array),2):
            SCREEN.blit(self.__rect_array[i], self.__rect_array[i+1])
        for button in self.__button_array:
            button.render(SCREEN, mouse)


    def draw_elements(self, type):
        if(type=='main_menu'):
            self.__main_menu()   
            return 
        if(type=='setup'):
            self.__setup()
            return
        if(type=='play'):
            self.__play()
            return
        if(type=='placement'):
            self.__placement()
            return
    
    def __placement(self):
         # setup labels for the boards
        placement_board_label = get_font(30).render("Board Setup", True, "White")
        placement_board_label_rect = placement_board_label.get_rect(center=(425, 100))
    
        # Create a confirm button
        confirm_button = Button(image=pygame.image.load("assets/ConfirmButton.png"), pos=(1000, 225))
        confirm_button = TextButton(confirm_button, text="Place", font=get_font(20))

         # Make a quit button
        quit_button = Button(image=pygame.image.load("assets/quit.png"), pos=(1000, 25))
        quit_button = TextButton(quit_button, text="QUIT", font=get_font(20))
        
        
        rotate_button = Button(image=pygame.image.load("assets/ConfirmButton.png"), pos=(1000, 150))
        rotate_button = TextButton(rotate_button, text="Rotate", font=get_font(20))
        
        for button in [quit_button, confirm_button, rotate_button]:
            self.__button_array.append(button)
        
        for element in [placement_board_label, placement_board_label_rect]:
            self.__rect_array.append(element)
        
    '''
    def __setup(self):
        text = get_font(70).render("SETUP YOUR SHIPS", True, "White")
        text_rect = text.get_rect(center=(650, 100))
        #placeholder text
        placeholder1_text = get_font(24).render("This function has not been implemented yet for this prototype.", True,"White")
        placeholder2_text = get_font(24).render("Please continue to game.", True, "White")
        placeholder3_text = get_font(24).render("All ships will be 1x1 and placed randomly", True, "White")

        placeholder1_rect = placeholder1_text.get_rect(center=(650, 300))
        placeholder2_rect = placeholder2_text.get_rect(center=(650, 350))
        placeholder3_rect = placeholder3_text.get_rect(center=(650, 400))
        #draw text and placeholders
        text = get_font(70).render("SETUP YOUR SHIPS", True, "White")
        text_rect = text.get_rect(center=(650, 100))
        
        # Continue to gameplay button
        continue_button = Button(image=base_button_image, pos=(650, 550))
        continue_button = TextButton(continue_button, text="CONTINUE", font=get_font(60))
        self.__button_array.append(continue_button)
        for element in [text, text_rect,placeholder1_text,placeholder2_text,placeholder3_text,placeholder1_rect,placeholder2_rect,placeholder3_rect,]:
            self.__rect_array.append(element)
    '''
    
        
    def __main_menu(self):
        text = get_font(100).render("BATTLESHIP", True, "#b68f40")
        text_rect = text.get_rect(center=(650, 100))

        play_button = Button(image=base_button_image, pos=(650, 250))
        play_button = ReactiveButton(play_button, hover_surface=hovered_button_image,
                                 active_surface=hovered_button_image)
        play_button = TextButton(play_button, text="PLAY", font=get_font(75))

        quit_button = Button(image=base_button_image, pos=(650, 550))
        quit_button = ReactiveButton(quit_button, hover_surface=hovered_button_image,
                                 active_surface=hovered_button_image)
        quit_button = TextButton(quit_button, text="QUIT", font=get_font(75))
        SCREEN.blit(text, text_rect)
        for button in [play_button, quit_button]:
            self.__button_array.append(button)
        for element in [text,text_rect]:
            self.__rect_array.append(element)
        
        
        
            
        
     
    def __play(self):
        # setup labels for the boards
        opponent_board_label = get_font(30).render("OPPONENT'S BOARD", True, "White")
        opponent_board_label_rect =opponent_board_label.get_rect(center=(425, 100))

        my_board_label = get_font(30).render("MY BOARD", True, "White")
        my_board_label_rect = my_board_label.get_rect(center=(1000, 325))
        
        # Create text
        select_text = get_font(15).render("YOU HAVE SELECTED:", True, "White")
        select_text_rect = select_text.get_rect(center=(1000, 150))
    
        # Create a confirm button
        confirm_button = Button(image=pygame.image.load("assets/ConfirmButton.png"), pos=(1000, 250))
        confirm_button = TextButton(confirm_button, text="FIRE", font=get_font(20))
        
        # Make a quit button
        quit_button = Button(image=pygame.image.load("assets/quit.png"), pos=(1000, 25))
        quit_button = TextButton(quit_button, text="QUIT", font=get_font(20))
        
        for button in [confirm_button, quit_button]:
            self.__button_array.append(button)
        for element in [opponent_board_label,opponent_board_label_rect,my_board_label,my_board_label_rect,select_text, select_text_rect]:
            self.__rect_array.append(element)
        
        
    async def set_active_cell(self,mouse,__player2):
        if __player2.board.get_cell_mouse(mouse) is not None:
            self.active_cell = __player2.board.get_cell_mouse(mouse)
            return True
        return False
    
    def endgamescreen(self, winner):
        text = get_font(100).render(winner + " WINS!", True, '#b68f40')
        text_rect = text.get_rect(center=(650, 100))
        quit_button = Button(image=pygame.image.load("assets/navy_button.png"), pos=(650, 550))
        quit_button = ReactiveButton(quit_button, hover_surface=pygame.image.load("assets/navy_button_hover.png"),
                                     active_surface=pygame.image.load("assets/navy_button_hover.png"))
        quit_button = TextButton(quit_button, text="QUIT", font=get_font(75))
        while (True):
            mouse = pygame.mouse.get_pos()
            SCREEN.blit(BG, (0, 0))
            SCREEN.blit(text, text_rect)
            for button in [quit_button]:
                button.render(SCREEN, mouse)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if quit_button.is_hovered(mouse):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()
            
    async def event_check(self, type, __player2, method,method2):
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__button_array.clear()
                self.__rect_array.clear()
                return 'quit'
            if event.type==pygame.KEYDOWN:
                if(type=='menu'):
                    global ai_game, create, join
                    if event.key == pygame.K_c:
                        ai_game = False
                        create =True
                        join=False
                    if event.key == pygame.K_j:
                        ai_game = False
                        create =False
                        join=True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.__button_array:
                    return
                #for menu screen
                if(type=='menu'):
                    if self.__button_array[0].is_hovered(mouse):
                        self.__button_array.clear()
                        self.__rect_array.clear()
                        return 'setup'
                    if self.__button_array[1].is_hovered(mouse):
                        self.__button_array.clear()
                        self.__rect_array.clear()
                        return 'quit'
                #for setup screen
                if(type=='setup'):
                    if self.__button_array[0].is_hovered(mouse):
                        self.__button_array.clear()
                        self.__rect_array.clear()
                        return 'play'
                #for playing screen
                if(type=='play'):
                    #if quit button
                    if not await self.set_active_cell(mouse,__player2):
                        if self.__button_array[1].is_hovered(mouse):
                            self.__button_array.clear()
                            self.__rect_array.clear()
                            return 'main_menu'
                        #if confirm button
                        if self.__button_array[0].is_hovered(mouse):
                            ret = await method(self.active_cell)
                            self.active_cell = None
                            self.__coord_text = None
                            self.__coord_text_rect = None
                            if(ret):
                                return 'action'
                            return
                        #if cell
                        if self.active_cell != None:
                            cell_coords = self.active_cell.coordinates
                            letter = Board.letters[cell_coords[0]]
                            num = cell_coords[1] + 1
                            self.__coord_text = get_font(15).render("({}, {})".format(letter, num), True, "White")
                            self.__coord_text_rect = self.__coord_text.get_rect(center=(1000, 200))
                if(type=='placement'):
                    if not method(mouse):
                        if self.__button_array[0].is_hovered(mouse):
                            self.__button_array.clear()
                            self.__rect_array.clear()
                            return 'main_menu'
                        if self.active_cell is not None and self.__button_array[1].is_hovered(mouse):
                            successful_placement=method2(self.ships_left, self.vertical,self.active_cell) 
                            self.active_cell = None
                            if successful_placement:
                                self.ships_left -=1
                                if (self.ships_left==0):
                                    self.__button_array.clear()
                                    self.__rect_array.clear()
                                return 'success'
                            
                                
                            self.__coord_text=None
                            self.__coord_text_rect=None
                        if self.__button_array[2].is_hovered(mouse):
                            self.vertical= not self.vertical
                            return
            
                
                        
                        
                        
                        
                      
