from MenuViews import MenuButtons

def DisableElement(ElementWrapper):
    ElementWrapper.internalbutton.hide()


def LoadAllViews( RoutingStack, container: [], manager):
    LoadMenuView( container, manager)
    LoadNewGameView(container, manager)
    ActivateView(RoutingStack, container, manager, 'Menu View', False)


def LoadMenuView(container: [], manager):
    NewGameButton = MenuButtons.NewGameOption('New game', 'Menu View', (50, 150), manager)
    container.append(NewGameButton)
    DisableElement(NewGameButton)
    LoadGameButton = MenuButtons.LoadGameOption('Load Game', 'Menu View', (50, 200), manager)
    container.append(LoadGameButton)
    DisableElement(LoadGameButton)
    TutorialButton = MenuButtons.TutorialOption('Tutorial', 'Menu View', (50, 400), manager)
    container.append(TutorialButton)
    DisableElement(TutorialButton)
    CreditsButton = MenuButtons.CreditsOption('Credits', 'Menu View', (50, 450), manager)
    container.append(CreditsButton)
    DisableElement(TutorialButton)
    QuitButton = MenuButtons.QuitOption('Quit', 'Menu View', (1150, 20), manager)
    container.append(QuitButton)
    DisableElement(QuitButton)

def LoadNewGameView(container: [], manager):
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


def ActivateView(RoutingStack, container: [], manager, View, isback: bool):
    for element in container:
        if element.view == View:
            element.internalbutton.show()
    if not isback:
        RoutingStack.append(View)
