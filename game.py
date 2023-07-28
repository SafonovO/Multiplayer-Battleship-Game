import sys
import time
import pygame
import asyncio

from board.board import Board
from game_manager import BG, SCREEN, GameManager
from server import Server

BOARD_SIZE = 8
NUM_SHIPS = 3

# Create a pygame window as a global constant
pygame.init()
pygame.display.set_caption("Menu")

manager = GameManager()
ai_game=True
join=False
create=False

server=None
async def placement(ship_count, game_size):
    # Track the orientation of the ship we are about to place
    # vertical = True by default
    ships_left = ship_count

    # create a game using the manager
    await manager.create_game(ai_game=ai_game,ship_count=ship_count,game_size= game_size,create=create, join=join)


    manager.draw('placement')

    while ships_left > 0:
        mouse = pygame.mouse.get_pos()
        
        manager.render(False, True)
        #manager.update_placement()
        # active cell is teh cell we are clicking on
        if manager.get_active_cell() != None:
            '''
            We have selected a cell.
            First, display the cell as text on screen.
            If the user then clicks FIRE, we call the game
            manager to execute the fire
            Here, I want to draw all the cells that will be occupied
            by the ship i'm about to place.
            IF there is a conflict, i will draw  the ship's cells in red
            if there is no conflict, the ship will be drawn in green
            there is a conflict IF:
                - one or more cells that this ship will occupy is already
                occupied by some ship
                - one or more cells that this ship will occupy exceeds the
                boundaries of the board
            If the user attempts to place a ship in an invlaid position,
            simply do nothing
            '''
            manager.preview_ship(ships_left)
        pygame.display.flip()
        event = await manager.event('placement')
        if(event=='main_menu'):
            main_menu()
        if(event=='quit'):
            quit_game()
        if(event=='success'):
            ships_left-=1
        
    await play()



async def play():
    '''
    Opponents board

    constructor takes location, rectangle size, and screen

    location will be (150, 100) (for now, might change)

    rectangle size will be 600 (for now)

    These parameters are all subject to change and
    their true values can be found below

    New addition: boards take a boolean parameter
    "display" which tells the draw function if it
    should display the true locations of the ships.

    Opponent's board should display, my board should not

    update: im making my board smaller and shifting it downwards
    to make room for the text headings
    '''
    opponent_board = Board(size=BOARD_SIZE, num_ships=NUM_SHIPS, coords=(150, 150), width=550, display=False)
    opponent_board.build_board()

    opponent_board.place_ships()
    # opponent_board.print_cells()

    '''
    Build a board for my own pieces

    My board will be 600 wide

    location will be at 150 + 700, 100

    My board should be much smaller than opponent's board
    since it is not the main focus
    '''
    my_board = Board(size=BOARD_SIZE, num_ships=NUM_SHIPS, coords=(850, 375), width=300, display=True)
    my_board.build_board()
    my_board.place_ships()

    '''
    the screen is 1700 wide and 800 tall.

    First, draw a gigantic rectangle to represent the playing surface.
    This rectangle should be 1500 wide and 700 tall. The background
    should be symmetrical around it, so its position should be at
    (100, 50)
    '''

    
    manager.draw('play')
    change_turn = True if join else False
    
    while True:
        #renders screen
        manager.update_boards()
        
        manager.render(True,True)
        
        if manager.client:
            await asyncio.sleep(0.1)
            
        # draw opponents board
        if change_turn:
            change_turn = False
            await manager.change_turn()
            continue

        action=await manager.event('play')
        if(action=='main_menu'):
            await main_menu()
        if(action=='action'):
            change_turn = True
        #pygame.display.update()
        pygame.display.flip()
        
        

'''
def setup():
    # Ship setup screen
    # Render text
    manager.draw('setup')
    while True:
        #render screen
        manager.render(False)
        # get events
        action=manager.event('setup')
        if(action=='play'):
            play()
        pygame.display.update()
'''

async def main_menu():
    # The loop for the main menu
    # render menu text, buttons
    manager.draw("main_menu")
    while True:
        #render the screen elements
        manager.render(False,False)

        # get events
        action =await manager.event('menu')
        if(action=='quit'):
            quit_game()
        elif(action=='setup'):
            await placement(8, 8)
        pygame.display.update()

def quit_game():
    pygame.quit()
    sys.exit()
    
asyncio.run(main_menu())
