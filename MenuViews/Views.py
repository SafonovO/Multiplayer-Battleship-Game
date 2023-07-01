from MenuViews import MenuButtons


def DisableElement(ElementWrapper):
    ElementWrapper.internalbutton.hide()


def LoadAllViews(container: [], manager):
    LoadMenuView(container, manager)
    LoadNewGameView(container, manager)
    ActivateView(container,manager,'Menu View')


def LoadMenuView(container: [], manager):
    NewGameButton = MenuButtons.NewGameOption('New game', 'Menu View', (150, 150), manager)
    container.append(NewGameButton)
    DisableElement(NewGameButton)
    LoadGameButton = MenuButtons.LoadGameOption('Load Game', 'Menu View', (150, 200), manager)
    container.append(LoadGameButton)
    DisableElement(LoadGameButton)
    TutorialButton = MenuButtons.TutorialOption('Tutorial', 'Menu View', (150, 400), manager)
    container.append(TutorialButton)
    DisableElement(TutorialButton)
    CreditsButton = MenuButtons.CreditsOption('Credits', 'Menu View', (150, 450), manager)
    container.append(CreditsButton)
    DisableElement(TutorialButton)


def LoadNewGameView(container: [], manager):
    AiGameButton = MenuButtons.SinglePlayerOption('Play vs AI', 'New Game View', (620, 170), manager)
    container.append(AiGameButton)
    DisableElement(AiGameButton)
    CreateGameButton = MenuButtons.CreateGameOption('Create Game', 'New Game View', (620, 220), manager)
    container.append(CreateGameButton)
    DisableElement(CreateGameButton)
    JoinGameButton = MenuButtons.JoinGameOption('Join Game', 'New Game View', (620, 270), manager)
    container.append(JoinGameButton)
    DisableElement(JoinGameButton)
    BackButton = MenuButtons.BackOption('Back', 'New Game View', (620, 320), manager)
    container.append(BackButton)
    DisableElement(BackButton)

def ActivateView(container: [], manager, View):
    for element in container:
        if element.view == View:
            element.internalbutton.show()
