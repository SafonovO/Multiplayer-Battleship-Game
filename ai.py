'''
Class for the AI opponent. 
'''


class AI:
    '''
    Guesses that reveal part of a ship will have those coordinates placed in revealed.
    Subsequent guesses will be to coordinates adjacent to revealed coordinates.
    Once an entire ship is revealed, those coordinates will be added to guessed and 
    removed from revealed.
    '''
    revealed, guessed = [], []

    def guess() -> bool:
        pass

    def place_ships() -> bool:
        pass

    def use_ability() -> bool:
        pass
