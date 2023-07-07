import pygame
import sys
from button import Button
from board import Board

# Create a pygame window as a global constant
pygame.init()

SCREEN = pygame.display.set_mode((1700, 800))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")




def get_font(size): # Returns Press-Start-2P in the desired size
	return pygame.font.Font("assets/font.ttf", size)

def play():
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
	'''
	opponent_board = Board(size=8, num_ships=8, coords=(150, 100), width=600, display=False)
	opponent_board.build_board()

	opponent_board.place_ships()
	#opponent_board.print_cells()

	'''
	Build a board for my own pieces

	My board will be 600 wide

	location will be at 150 + 700, 100 + 700
	'''
	my_board = Board(size=8, num_ships=8, coords=(850, 100), width=600, display=True)
	my_board.build_board()
	my_board.place_ships()
	'''
	Logic Time:

	the screen is 1700 wide and 800 tall.

	First, draw a gigantic rectangle to represent the playing surface.
	This rectangle should be 1500 wide and 700 tall. The background
	should be symmetrical around it, so its position should be at
	(100, 50)
	'''
	playing_surface = pygame.Rect(100, 50, 1500, 700)

	while True:
		mouse = pygame.mouse.get_pos()

		# Draw the backgroudn
		SCREEN.blit(BG, (0, 0))

		# Draw the playing surface as described above
		pygame.draw.rect(SCREEN, "#042574", playing_surface)

		# draw opponents board
		opponent_board.draw_board(SCREEN)

		# draw my board
		my_board.draw_board(SCREEN)


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				active_cell = opponent_board.get_active_cell(mouse)

				# active cell is teh cell we are clicking on
				if active_cell != None:
					# Fire on that cell
					manager.action(active_cell)

		#pygame.display.update()
		pygame.display.flip()


def setup():
	# Ship setup screen

	# Render text
	SETUP_TEXT = get_font(70).render("SETUP YOUR SHIPS", True, "White")
	SETUP_RECT = SETUP_TEXT.get_rect(center=(850, 100))

	# Placeholder text for now
	placeholder1_text = get_font(20).render("This function has not been implemented yet for this prototype.", True, "White")
	placeholder2_text = get_font(30).render("Please continue to game.", True, "White")
	placeholder3_text = get_font(30).render("All ships will be 1x1 and placed randomly", True, "White")


	placeholder1_rect = placeholder1_text.get_rect(center=(850, 300))
	placeholder2_rect = placeholder2_text.get_rect(center=(850, 350))
	placeholder3_rect = placeholder3_text.get_rect(center=(850, 400))


	# Continue to gameplay button
	CONTINUE_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(850, 550), 
						text_input="CONTINUE", font=get_font(60), base_color="White", hovering_color="#d7fcd4")

	while True:
		# paint background
		SCREEN.blit(BG, (0, 0))

		# get mouse position
		SETUP_MOUSE_POS = pygame.mouse.get_pos()


		SCREEN.blit(SETUP_TEXT, SETUP_RECT)

		SCREEN.blit(placeholder1_text, placeholder1_rect)
		SCREEN.blit(placeholder2_text, placeholder2_rect)
		SCREEN.blit(placeholder3_text, placeholder3_rect)

		CONTINUE_BUTTON.changeColor(SETUP_MOUSE_POS)
		CONTINUE_BUTTON.update(SCREEN)
		
		# get events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			# if we clicked, find out if we clicked on a button and execute that buttons action
			if event.type == pygame.MOUSEBUTTONDOWN:
				if CONTINUE_BUTTON.checkForInput(SETUP_MOUSE_POS):
					play()

		pygame.display.update()






def main_menu():
	# The loop for the main menu
	# render menu text, buttons
	MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
	MENU_RECT = MENU_TEXT.get_rect(center=(850, 100))

	PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(850, 250), 
						text_input="PLAY", font=get_font(75), base_color="White", hovering_color="#d7fcd4")
	
	QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(850, 550), 
						text_input="QUIT", font=get_font(75), base_color="White", hovering_color="#d7fcd4")
	while True:
		# Draw the background
		SCREEN.blit(BG, (0, 0))

		# Get mouse position
		MENU_MOUSE_POS = pygame.mouse.get_pos()

		# draw meny text, buttons
		SCREEN.blit(MENU_TEXT, MENU_RECT)

		for button in [PLAY_BUTTON, QUIT_BUTTON]:
			button.changeColor(MENU_MOUSE_POS)
			button.update(SCREEN)
		
		# get events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			# if we clicked, find out if we clicked on a button and execute that buttons action
			if event.type == pygame.MOUSEBUTTONDOWN:
				if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
					setup()

				if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
					pygame.quit()
					# run = False
					sys.exit()

		pygame.display.update()


main_menu()
