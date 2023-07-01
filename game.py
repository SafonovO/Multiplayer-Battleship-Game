import pygame
import pygame_gui

from MenuViews import Views


def main():
    pygame.init()
    ElementContainer = []
    pygame.display.set_caption("Battleship")
    pygame.display.set_mode((1280, 720))
    window_surface = pygame.display.set_mode((1280, 720))
    background = pygame.Surface((1280, 720))
    background.fill(pygame.Color('#000000'))

    manager = pygame_gui.UIManager((1280, 720))

    clock = pygame.time.Clock()
    running = True
    Views.LoadAllViews(ElementContainer, manager)
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if issubclass(type(event.ui_element), pygame_gui.elements.UIButton):
                    ElementContainer[manager.root_container.elements.index(event.ui_element)].execute_action(
                        ElementContainer)

        manager.update(time_delta)
        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    main()
