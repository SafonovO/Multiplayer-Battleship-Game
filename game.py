import pygame
import sys
from button import Button, ReactiveButton, TextButton
from board import Board
from fonts import get_font
from game_manager import GameManager

# Create a pygame window as a global constant
pygame.init()

SCREEN = pygame.display.set_mode((1300, 800))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

base_button_iamge = pygame.image.load("assets/navy_button.png")
hovered_button_image = pygame.image.load("assets/navy_button_hover.png")

manager = GameManager()

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

	update: im making my board smaller and shifting it downwards
	to make room for the text headings
	'''
	opponent_board = Board(size=8, num_ships=8, coords=(150, 150), width=550, display=False)
	opponent_board.build_board()

	opponent_board.place_ships()
	#opponent_board.print_cells()

	'''
	Build a board for my own pieces

	My board will be 600 wide

	location will be at 150 + 700, 100

	My board should be much smaller than opponent's board
	since it is not the main focus
	'''
	my_board = Board(size=8, num_ships=8, coords=(850, 375), width=300, display=True)
	my_board.build_board()
	my_board.place_ships()

	'''
	the screen is 1700 wide and 800 tall.

	First, draw a gigantic rectangle to represent the playing surface.
	This rectangle should be 1500 wide and 700 tall. The background
	should be symmetrical around it, so its position should be at
	(100, 50)
	'''

	playing_surface = pygame.Rect(100, 50, 1100, 700)

	# setup labels for the boards
	opponent_board_label = get_font(30).render("OPPONENT'S BOARD", True, "White")
	opponent_board_label_rect = opponent_board_label.get_rect(center=(425, 100))

	my_board_label = get_font(30).render("MY BOARD", True, "White")
	my_board_label_rect = my_board_label.get_rect(center=(1000, 325))
	
	# create a game using the manager
	manager.create_game([my_board, opponent_board])

	# Create a confirm button
	confirm_button = Button(image=pygame.image.load("assets/ConfirmButton.png"), pos=(1000, 250))
	confirm_button = TextButton(confirm_button, text="FIRE", font=get_font(20))

	# Create text
	select_text = get_font(15).render("YOU HAVE SELECTED:", True, "White")
	select_text_rect = select_text.get_rect(center=(1000, 150))

	# Coord text
	coord_text = None
	coord_text_rect = None

	# track the selected cell
	active_cell = None

	# Make a quit button
	quit_button = Button(image=pygame.image.load("assets/quit.png"), pos=(1000, 25))
	quit_button = TextButton(quit_button, text="QUIT", font=get_font(20))

	update = False

	while True:
		mouse = pygame.mouse.get_pos()

		# Draw the backgroudn
		SCREEN.blit(BG, (0, 0))

		# Draw the playing surface as described above
		pygame.draw.rect(SCREEN, "#042574", playing_surface)

		# Draw the labels
		SCREEN.blit(opponent_board_label, opponent_board_label_rect)
		SCREEN.blit(my_board_label, my_board_label_rect)

		SCREEN.blit(select_text, select_text_rect)

		# draw opponents board
		opponent_board.draw_board(SCREEN)

		# draw my board
		my_board.draw_board(SCREEN)

		# draw the confirm button
		confirm_button.render(SCREEN, mouse)

		quit_button.render(SCREEN, mouse)

		# draw the coord text if it is not None
		if coord_text != None and coord_text_rect != None:
			SCREEN.blit(coord_text, coord_text_rect)

		# Draw active cell if it is not None
		if active_cell != None:
			active_cell.draw_selected_cell(SCREEN)

		if not update:
			manager.action(None)
		update = False

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if opponent_board.get_active_cell(mouse) != None: 
					active_cell = opponent_board.get_active_cell(mouse)

				# if we hit confirm, fire with the manager
				if confirm_button.is_hovered(mouse):
					manager.action(active_cell)
					update = True
					active_cell = None

					coord_text = None
					coord_text_rect = None

				# active cell is teh cell we are clicking on
				if active_cell != None:
					'''
					We have selected a cell.

					First, display the cell as text on screen.

					If the user then clicks FIRE, we call the game
					manager to execute the fire
					'''
					cell_coords = active_cell.coordinates
					letter = Board.letters[cell_coords[0]]
					num = cell_coords[1]+1

					coord_text = get_font(15).render("({}, {})".format(letter, num), True, "White")
					coord_text_rect = coord_text.get_rect(center=(1000, 200))

				# the active cell will be drawn on the next loop
				if quit_button.is_hovered(mouse):
					# return to main menu
					main_menu()
		#pygame.display.update()
		pygame.display.flip()


def setup():
	# Ship setup screen

	# Render text
	text = get_font(70).render("SETUP YOUR SHIPS", True, "White")
	text_rect = text.get_rect(center=(650, 100))

	# Placeholder text for now
	placeholder1_text = get_font(24).render("This function has not been implemented yet for this prototype.", True, "White")
	placeholder2_text = get_font(24).render("Please continue to game.", True, "White")
	placeholder3_text = get_font(24).render("All ships will be 1x1 and placed randomly", True, "White")


	placeholder1_rect = placeholder1_text.get_rect(center=(650, 300))
	placeholder2_rect = placeholder2_text.get_rect(center=(650, 350))
	placeholder3_rect = placeholder3_text.get_rect(center=(650, 400))


	# Continue to gameplay button
	continue_button = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(650, 550))
	continue_button = TextButton(continue_button, text="CONTINUE", font=get_font(60))

	while True:
		# paint background
		SCREEN.blit(BG, (0, 0))

		# get mouse position
		mouse = pygame.mouse.get_pos()


		SCREEN.blit(text, text_rect)

		SCREEN.blit(placeholder1_text, placeholder1_rect)
		SCREEN.blit(placeholder2_text, placeholder2_rect)
		SCREEN.blit(placeholder3_text, placeholder3_rect)

		continue_button.render(SCREEN, mouse)
		
		# get events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			# if we clicked, find out if we clicked on a button and execute that buttons action
			if event.type == pygame.MOUSEBUTTONDOWN:
				if continue_button.is_hovered(mouse):
					play()

		pygame.display.update()






def main_menu():
	# The loop for the main menu
	# render menu text, buttons
	text = get_font(100).render("BATTLESHIP", True, "#b68f40")
	text_rect = text.get_rect(center=(650, 100))

	play_button = Button(image=base_button_iamge, pos=(650, 250))
	play_button = ReactiveButton(play_button, hover_surface=hovered_button_image,
					active_surface=hovered_button_image)
	play_button = TextButton(play_button, text="PLAY", font=get_font(75))
	
	quit_button = Button(image=base_button_iamge, pos=(650, 550))
	quit_button = ReactiveButton(quit_button, hover_surface=hovered_button_image,
					active_surface=hovered_button_image)
	quit_button = TextButton(quit_button, text="QUIT", font=get_font(75))

	while True:
		# Draw the background
		SCREEN.blit(BG, (0, 0))

		# Get mouse position
		mouse = pygame.mouse.get_pos()

		# draw meny text, buttons
		SCREEN.blit(text, text_rect)

		for button in [play_button, quit_button]:
			button.render(SCREEN, mouse)
		
		# get events
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()

			# if we clicked, find out if we clicked on a button and execute that buttons action
			if event.type == pygame.MOUSEBUTTONDOWN:
				if play_button.is_hovered(mouse):
					setup()

				if quit_button.is_hovered(mouse):
					pygame.quit()
					# run = False
					sys.exit()

		pygame.display.update()


main_menu()
