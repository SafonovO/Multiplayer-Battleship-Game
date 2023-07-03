import pygame
import pygame_gui
import os
from menu_views import views
from assets import fonts

def main():
    pygame.init()
    ElementContainer = []
    RoutingStack = []
    pygame.display.set_caption("Battleship")
    pygame.display.set_mode((1280, 720))
    window_surface = pygame.display.set_mode((1280, 720))
    background = pygame.image.load(os.path.join('assets','background.png'))

    manager = pygame_gui.UIManager((1280, 720), os.path.join('assets','style.json'))
    manager.preload_fonts(fonts.font_list)
    clock = pygame.time.Clock()
    running = True
    views.LoadAllViews(RoutingStack, ElementContainer, manager)
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if issubclass(type(event.ui_element), pygame_gui.elements.UIButton):
                    next(x for x in ElementContainer if x.internalelement == event.ui_element).execute_action(
                        RoutingStack,
                        ElementContainer)

        manager.update(time_delta)
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
