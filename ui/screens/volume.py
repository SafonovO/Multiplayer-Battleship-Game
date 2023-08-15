from game_config import MAX_VOLUME, MIN_VOLUME
import pygame
from ui.colours import Colours
from ui.elements import make_back_button, make_button, plus_button_image, minus_button_image, quit_button_image
from ui.router import Screen
from ui.sounds import click_sound
from ui.text import Text


class Volume(Screen):
    def __init__(self, manager) -> None:
        super().__init__(manager)
        self.draw_background = True

        volume_text = Text("Volume", (650, 100), 50, Colours.GOLD)
        bg_music_text = Text("Background music:",
                             (400, 250), 30, Colours.WHITE)
        sfx_text = Text("Game sound effects:", (395, 350), 30, Colours.WHITE)
        click_sound_text = Text("Click sound effect:",
                                (402, 450), 30, Colours.WHITE)

        self.bg_music_val = Text(
            str(manager.get_volume("bg")), (675, 245), 40, Colours.WHITE)
        self.sfx_val = Text(str(manager.get_volume("sfx")),
                            (675, 345), 40, Colours.WHITE)
        self.click_sound_val = Text(
            str(manager.get_volume("click")), (675, 445), 40, Colours.WHITE)
        
        self.error_text = Text("", (650, 550), 30, Colours.RED)

        self.bg_inc = make_button(750, 250, "", 0, image=plus_button_image)
        self.bg_dec = make_button(600, 250, "", 0, image=minus_button_image)
        self.sfx_inc = make_button(750, 350, "", 0, image=plus_button_image)
        self.sfx_dec = make_button(600, 350, "", 0, image=minus_button_image)
        self.click_inc = make_button(750, 450, "", 0, image=plus_button_image)
        self.click_dec = make_button(600, 450, "", 0, image=minus_button_image)

        self.bg_mute = make_button(
            900, 250, "MUTE", 20, image=quit_button_image)
        self.sfx_mute = make_button(
            900, 350, "MUTE", 20, image=quit_button_image)
        self.click_mute = make_button(
            900, 450, "MUTE", 20, image=quit_button_image)

        self.back_button = make_back_button()

        self.inc_buttons = [self.bg_inc, self.sfx_inc, self.click_inc]
        self.dec_buttons = [self.bg_dec, self.sfx_dec, self.click_dec]
        self.mute_buttons = [self.bg_mute, self.sfx_mute, self.click_mute]

        self.button_array = [self.back_button] + \
            self.inc_buttons + self.dec_buttons + self.mute_buttons
        self.text_array = [volume_text,
                           bg_music_text,
                           sfx_text,
                           click_sound_text,
                           self.bg_music_val,
                           self.sfx_val,
                           self.click_sound_val,
                           self.error_text]

    def handle_event(self, event, mouse, router, manager):
        def update_labels():
            self.bg_music_val.value = str(manager.get_volume("bg"))
            self.sfx_val.value = str(manager.get_volume("sfx"))
            self.click_sound_val.value = str(manager.get_volume("click"))
            self.error_text.value = ""
            mute_buttons = zip(self.mute_buttons, labels)
            for button, label in mute_buttons:
                if manager.volumes[label] == 0:
                    button.set_text("UNMUTE")
                else:
                    button.set_text("MUTE")

        if event.type == pygame.MOUSEBUTTONDOWN:
            labels = ["bg", "sfx", "click"]
            inc_buttons = zip(self.inc_buttons, labels)
            for button, label in inc_buttons:
                if button.is_hovered(mouse):
                    if manager.volumes[label] != MAX_VOLUME:
                        click_sound.play()
                        manager.change_volume(label, increase=True)
                        update_labels()
                    else:
                        self.error_text.value = f"Maximum volume is {MAX_VOLUME}"
                    return

            dec_buttons = zip(self.dec_buttons, labels)
            for button, label in dec_buttons:
                if button.is_hovered(mouse):
                    if manager.volumes[label] != MIN_VOLUME:
                        click_sound.play()
                        manager.change_volume(label, increase=False)
                        update_labels()
                    else:
                        self.error_text.value = f"Minimum volume is {MIN_VOLUME}"
                    return

            mute_buttons = zip(self.mute_buttons, labels)
            for button, label in mute_buttons:
                if button.is_hovered(mouse):
                    click_sound.play()
                    if manager.volumes[label] != MIN_VOLUME:
                        manager.change_volume(label, mute=True)
                    else:
                        manager.change_volume(label, unmute=True)
                    update_labels()
                    return

            if self.back_button.is_hovered(mouse):
                click_sound.play()
                return router.navigate_back()
