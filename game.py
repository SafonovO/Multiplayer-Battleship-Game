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
	# Make a board
	board = Board(8, 8)


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


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
					main_menu()

		pygame.display.update()

def setup():
	# Ship setup screen

	# Render text
	SETUP_TEXT = get_font(70).render("SETUP YOUR SHIPS", True, "White")
	SETUP_RECT = SETUP_TEXT.get_rect(center=(640, 100))

	# Continue to gameplay button
	CONTINUE_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 550), 
						text_input="CONTINUE", font=get_font(75), base_color="White", hovering_color="#d7fcd4")

	while True:
		# paint background
		SCREEN.blit(BG, (0, 0))

		# get mouse position
		SETUP_MOUSE_POS = pygame.mouse.get_pos()


		SCREEN.blit(SETUP_TEXT, SETUP_RECT)

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
	MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

	PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
						text_input="PLAY", font=get_font(75), base_color="White", hovering_color="#d7fcd4")
	
	QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
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


play()