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
    LoadSinglePlayerGame(container,manager)
    ActivateView(RoutingStack, container, manager, 'Menu View', False)


def LoadMenuView(container: [], manager):
    GameTitle = text.Label('<font size=6.5>B\nA\nT\nT\nL\nE\nS\nH\nI\nP</font>', 'Menu View', (-2, 0), (60, 720),
                           '@menu_title', manager)
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

    QuitButton = menu_options.QuitOption('Quit', 'Menu View', (1150, 10), manager)
    container.append(QuitButton)
    DisableElement(QuitButton)


def LoadNewGameView(container: [], manager):
    BackGround = shapes.Rectangle('New Game View', (500, 100), (270, 400), '@rectangle', manager)
    container.append(BackGround)
    DisableElement(BackGround)

    GameTitle = text.Label('<font size=5>B A T T L E S H I P</font>', 'New Game View', (510, 110), (250, 60),
                           '@menu_title2', manager)
    container.append(GameTitle)
    DisableElement(GameTitle)

    AiGameButton = menu_options.SinglePlayerOption('Play vs AI', 'New Game View', (570, 210), manager)
    container.append(AiGameButton)
    DisableElement(AiGameButton)

    CreateGameButton = menu_options.CreateGameOption('Create Game', 'New Game View', (570, 260), manager)
    container.append(CreateGameButton)
    DisableElement(CreateGameButton)

    JoinGameButton = menu_options.JoinGameOption('Join Game', 'New Game View', (570, 310), manager)
    container.append(JoinGameButton)
    DisableElement(JoinGameButton)

    BackButton = menu_options.BackOption('Back', 'New Game View', (570, 420), manager)
    container.append(BackButton)
    DisableElement(BackButton)

    QuitButton = menu_options.QuitOption('Quit', 'New Game View', (1150, 10), manager)
    container.append(QuitButton)
    DisableElement(QuitButton)


def LoadSinglePlayerView(container: [], manager):
    BackGround = shapes.Rectangle('Single Player View', (300, 100), (700, 400), '@rectangle', manager)
    container.append(BackGround)
    DisableElement(BackGround)

    GameTitle = text.Label('<font size=5>Game Settings</font>', 'Single Player View', (480, 110), (350, 40),
                           '@menu_title2', manager)
    container.append(GameTitle)
    DisableElement(GameTitle)

    DifficultyLabel = text.Label('<font size=4.5>Difficulty</font>', 'Single Player View', (310, 170), (140, 40),
                                 '@label', manager)
    container.append(DifficultyLabel)
    DisableElement(DifficultyLabel)

    EasyDifficultyButton = menu_options.DifficultyOption('Easy', 'Single Player View', (460, 170), manager)
    container.append(EasyDifficultyButton)
    DisableElement(EasyDifficultyButton)

    MediumDifficultyButton = menu_options.DifficultyOption('Medium', 'Single Player View', (640, 170), manager)
    container.append(MediumDifficultyButton)
    DisableElement(MediumDifficultyButton)

    HardDifficultyButton = menu_options.DifficultyOption('Hard', 'Single Player View', (820, 170), manager)
    container.append(HardDifficultyButton)
    DisableElement(HardDifficultyButton)

    SmallBoardButton = menu_options.BoardSizeOption('6x6', 'Single Player View', (460, 230), manager)
    container.append(SmallBoardButton)
    DisableElement(SmallBoardButton)

    MediumBoardButton = menu_options.BoardSizeOption('7x7', 'Single Player View', (640, 230), manager)
    container.append(MediumBoardButton)
    DisableElement(MediumBoardButton)

    LargeBoardButton = menu_options.BoardSizeOption('8x8', 'Single Player View', (820, 230), manager)
    container.append(LargeBoardButton)
    DisableElement(LargeBoardButton)

    GameSizeLabel = text.Label('<font size=4.5>Game Size</font>', 'Single Player View', (310, 230), (140, 40),
                               '@label', manager)
    container.append(GameSizeLabel)
    DisableElement(GameSizeLabel)

    QuitButton = menu_options.QuitOption('Quit', 'Single Player View', (1150, 10), manager)
    container.append(QuitButton)
    DisableElement(QuitButton)

    StartButton = menu_options.StartSinglePlayerOption('Start Game', 'Single Player View', (580, 350), manager)
    container.append(StartButton)
    DisableElement(StartButton)

    BackButton = menu_options.BackOption('Back', 'Single Player View', (580, 420), manager)
    container.append(BackButton)
    DisableElement(BackButton)


def LoadSinglePlayerGame(container: [], manager):
    BackGround = shapes.Rectangle('Game View', (50, 30), (1180, 690), '@rectangle', manager)
    container.append(BackGround)
    DisableElement(BackGround)

    YourBoardLabel = text.Label('<font size=5>Your Board</font>', 'Game View', (240, 40), (140, 40),
                                 '@label', manager)
    container.append(YourBoardLabel)
    DisableElement(YourBoardLabel)

    OpponentBoardLabel = text.Label('<font size=5>Opponent`s Board</font>', 'Game View', (870, 40), (220, 40),
                                 '@label', manager)
    container.append(OpponentBoardLabel)
    DisableElement(OpponentBoardLabel)

    CardLabel = text.Label('<font size=5>Your Cards</font>', 'Game View', (80, 530), (140, 40),
                             '@label', manager)
    container.append(CardLabel)
    DisableElement(CardLabel)

    SaveButton = menu_options.SaveGameOption('Save Game', 'Game View', (980, 0), manager)
    container.append(SaveButton)
    DisableElement(SaveButton)

    MainMenuButton = menu_options.MainMenuOption('Main Menu', 'Game View', (855, 0), manager)
    container.append(MainMenuButton)
    DisableElement(MainMenuButton)

    QuitButton = menu_options.QuitOption('Quit', 'Game View', (1105, 0), manager)
    container.append(QuitButton)
    DisableElement(QuitButton)

    YourBoard = shapes.Rectangle('Game View', (90, 80), (450, 450), '@rectangle_board', manager)
    container.append(YourBoard)
    DisableElement(YourBoard)

    OpponentBoard = shapes.Rectangle('Game View', (740, 80), (450, 450), '@rectangle_board', manager)
    container.append(OpponentBoard)
    DisableElement(OpponentBoard)