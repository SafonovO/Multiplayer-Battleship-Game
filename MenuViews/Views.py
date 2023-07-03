import pygame_gui.core.drawable_shapes
import pygame
from MenuViews import MenuButtons
from Utilities import Shapes, Text

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
    GameTitle = Text.Label('<font size=6.5>B\nA\nT\nT\nL\nE\nS\nH\nI\nP</font>', 'Menu View', (0,0),(60,720),'@menu_title',manager)
    container.append(GameTitle)
    DisableElement(GameTitle)
    NewGameButton = MenuButtons.NewGameOption('New game', 'Menu View', (60, 150), manager)
    container.append(NewGameButton)
    DisableElement(NewGameButton)
    LoadGameButton = MenuButtons.LoadGameOption('Load Game', 'Menu View', (60, 200), manager)
    container.append(LoadGameButton)
    DisableElement(LoadGameButton)
    TutorialButton = MenuButtons.TutorialOption('Tutorial', 'Menu View', (60, 400), manager)
    container.append(TutorialButton)
    DisableElement(TutorialButton)
    CreditsButton = MenuButtons.CreditsOption('Credits', 'Menu View', (60, 450), manager)
    container.append(CreditsButton)
    DisableElement(TutorialButton)
    QuitButton = MenuButtons.QuitOption('Quit', 'Menu View', (1150, 20), manager)
    container.append(QuitButton)
    DisableElement(QuitButton)


def LoadNewGameView(container: [], manager):
    BackGround = Shapes.Rectangle('New Game View', (500, 100), (270, 400), '@rectangle', manager)
    container.append(BackGround)
    DisableElement(BackGround)
    AiGameButton = MenuButtons.SinglePlayerOption('Play vs AI', 'New Game View', (570, 170), manager)
    container.append(AiGameButton)
    DisableElement(AiGameButton)
    CreateGameButton = MenuButtons.CreateGameOption('Create Game', 'New Game View', (570, 220), manager)
    container.append(CreateGameButton)
    DisableElement(CreateGameButton)
    JoinGameButton = MenuButtons.JoinGameOption('Join Game', 'New Game View', (570, 270), manager)
    container.append(JoinGameButton)
    DisableElement(JoinGameButton)
    BackButton = MenuButtons.BackOption('Back', 'New Game View', (570, 320), manager)
    container.append(BackButton)
    DisableElement(BackButton)
    QuitButton = MenuButtons.QuitOption('Quit', 'New Game View', (1150, 20), manager)
    container.append(QuitButton)
    DisableElement(QuitButton)


def LoadSinglePlayerView(container: [], manager):
    BackGround = Shapes.Rectangle('Single Player View', (300,100),(700,400), '@rectangle' ,manager)
    container.append(BackGround)
    DisableElement(BackGround)
    EasyDifficultyButton = MenuButtons.DifficultyOption('Easy', 'Single Player View', (380, 170), manager)
    container.append(EasyDifficultyButton)
    DisableElement(EasyDifficultyButton)
    MediumDifficultyButton = MenuButtons.DifficultyOption('Medium', 'Single Player View', (580, 170), manager)
    container.append(MediumDifficultyButton)
    DisableElement(MediumDifficultyButton)
    HardDifficultyButton = MenuButtons.DifficultyOption('Hard', 'Single Player View', (780, 170), manager)
    container.append(HardDifficultyButton)
    DisableElement(HardDifficultyButton)
    SmallBoardButton = MenuButtons.BoardSizeOption('6x6', 'Single Player View', (380, 220), manager)
    container.append(SmallBoardButton)
    DisableElement(SmallBoardButton)
    MediumBoardButton = MenuButtons.BoardSizeOption('7x7', 'Single Player View', (580, 220), manager)
    container.append(MediumBoardButton)
    DisableElement(MediumBoardButton)
    LargeBoardButton = MenuButtons.BoardSizeOption('8x8', 'Single Player View', (780, 220), manager)
    container.append(LargeBoardButton)
    DisableElement(LargeBoardButton)
    QuitButton = MenuButtons.QuitOption('Quit', 'Single Player View', (1150, 20), manager)
    container.append(QuitButton)
    DisableElement(QuitButton)
    BackButton = MenuButtons.BackOption('Back', 'Single Player View', (580, 420), manager)
    container.append(BackButton)
    DisableElement(BackButton)