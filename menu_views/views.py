import pygame_gui.core.drawable_shapes
import pygame
from menu_views import menu_options
from utilities import shapes, text

def DisableElement(ElementWrapper):
    ElementWrapper.internalelement.hide()


def ActivateView(RoutingStack, container: [], manager, View, isback: bool):
    for element in container:
        if element.view == View:
            element.internalelement.show()
    if not isback:
        RoutingStack.append(View)


def LoadAllViews(RoutingStack, container: [], manager):
    LoadMenuView(container, manager)
    LoadNewGameView(container, manager)
    LoadSinglePlayerView(container, manager)
    ActivateView(RoutingStack, container, manager, 'Menu View', False)


def LoadMenuView(container: [], manager):
    GameTitle = text.Label('<font size=6.5>B\nA\nT\nT\nL\nE\nS\nH\nI\nP</font>', 'Menu View', (0,0),(60,720),'@menu_title',manager)
    container.append(GameTitle)
    DisableElement(GameTitle)
    NewGameButton = menu_options.NewGameOption('New game', 'Menu View', (60, 150), manager)
    container.append(NewGameButton)
    DisableElement(NewGameButton)
    LoadGameButton = menu_options.LoadGameOption('Load Game', 'Menu View', (60, 200), manager)
    container.append(LoadGameButton)
    DisableElement(LoadGameButton)
    TutorialButton = menu_options.TutorialOption('Tutorial', 'Menu View', (60, 400), manager)
    container.append(TutorialButton)
    DisableElement(TutorialButton)
    CreditsButton = menu_options.CreditsOption('Credits', 'Menu View', (60, 450), manager)
    container.append(CreditsButton)
    DisableElement(TutorialButton)
    QuitButton = menu_options.QuitOption('Quit', 'Menu View', (1150, 20), manager)
    container.append(QuitButton)
    DisableElement(QuitButton)


def LoadNewGameView(container: [], manager):
    BackGround = shapes.Rectangle('New Game View', (500, 100), (270, 400), '@rectangle', manager)
    container.append(BackGround)
    DisableElement(BackGround)
    AiGameButton = menu_options.SinglePlayerOption('Play vs AI', 'New Game View', (570, 170), manager)
    container.append(AiGameButton)
    DisableElement(AiGameButton)
    CreateGameButton = menu_options.CreateGameOption('Create Game', 'New Game View', (570, 220), manager)
    container.append(CreateGameButton)
    DisableElement(CreateGameButton)
    JoinGameButton = menu_options.JoinGameOption('Join Game', 'New Game View', (570, 270), manager)
    container.append(JoinGameButton)
    DisableElement(JoinGameButton)
    BackButton = menu_options.BackOption('Back', 'New Game View', (570, 320), manager)
    container.append(BackButton)
    DisableElement(BackButton)
    QuitButton = menu_options.QuitOption('Quit', 'New Game View', (1150, 20), manager)
    container.append(QuitButton)
    DisableElement(QuitButton)


def LoadSinglePlayerView(container: [], manager):
    BackGround = shapes.Rectangle('Single Player View', (300,100),(700,400), '@rectangle' ,manager)
    container.append(BackGround)
    DisableElement(BackGround)
    EasyDifficultyButton = menu_options.DifficultyOption('Easy', 'Single Player View', (380, 170), manager)
    container.append(EasyDifficultyButton)
    DisableElement(EasyDifficultyButton)
    MediumDifficultyButton = menu_options.DifficultyOption('Medium', 'Single Player View', (580, 170), manager)
    container.append(MediumDifficultyButton)
    DisableElement(MediumDifficultyButton)
    HardDifficultyButton = menu_options.DifficultyOption('Hard', 'Single Player View', (780, 170), manager)
    container.append(HardDifficultyButton)
    DisableElement(HardDifficultyButton)
    SmallBoardButton = menu_options.BoardSizeOption('6x6', 'Single Player View', (380, 220), manager)
    container.append(SmallBoardButton)
    DisableElement(SmallBoardButton)
    MediumBoardButton = menu_options.BoardSizeOption('7x7', 'Single Player View', (580, 220), manager)
    container.append(MediumBoardButton)
    DisableElement(MediumBoardButton)
    LargeBoardButton = menu_options.BoardSizeOption('8x8', 'Single Player View', (780, 220), manager)
    container.append(LargeBoardButton)
    DisableElement(LargeBoardButton)
    QuitButton = menu_options.QuitOption('Quit', 'Single Player View', (1150, 20), manager)
    container.append(QuitButton)
    DisableElement(QuitButton)
    BackButton = menu_options.BackOption('Back', 'Single Player View', (580, 420), manager)
    container.append(BackButton)
    DisableElement(BackButton)