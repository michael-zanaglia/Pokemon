# import pygame
# import pygame_menu
# import simpleaudio as sa

# class SoundManager:
#     def __init__(self, sound_path: str, volume: float = 1.0):
#         self.sound = sa.WaveObject.from_wave_file(sound_path)
#         self.volume = volume

#     def play(self):
#         play_obj = self.sound.play()
#         play_obj.wait_done()

# class MainMenu:
#     def __init__(self, window_size, fps_limit):
#         self.window_size = window_size
#         self.fps_limit = fps_limit
#         self.surface = pygame.display.set_mode(self.window_size)
#         self.clock = pygame.time.Clock()

#         # Crea il SoundManager come attributo della classe
#         self.sound_manager = SoundManager('Pokemon/graphique/Menu/music/pokemon_experienceW.wav', volume=0.5)

#         self.initialize_menu()

#     def initialize_menu(self):
#         main_menu_theme = pygame_menu.themes.THEME_ORANGE.copy()
#         main_menu_theme.set_background_color_opacity(0.5)

#         self.menu = pygame_menu.Menu(
#             height=self.window_size[1] * 0.7,
#             onclose=pygame_menu.events.EXIT,
#             theme=main_menu_theme,
#             title='Epic Menu',
#             width=self.window_size[0] * 0.8
#         )

#         # Rimuovi il percorso specifico per rendere il codice più generale e portatile

#         theme_bg_image = main_menu_theme.copy()
#         theme_bg_image.background_color = pygame_menu.BaseImage(
#             image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_CARBON_FIBER
#         )
#         theme_bg_image.title_font_size = 25
#         menu_with_bg_image = pygame_menu.Menu(
#             height=self.window_size[1] * 0.7,
#             onclose=pygame_menu.events.EXIT,
#             theme=theme_bg_image,
#             title='Menu with background image',
#             width=self.window_size[0] * 0.8
#         )
#         menu_with_bg_image.add.button('Back', pygame_menu.events.BACK)

#         widget_colors_theme = pygame_menu.themes.THEME_ORANGE.copy()
#         widget_colors_theme.widget_margin = (0, 10)
#         widget_colors_theme.widget_padding = 0
#         widget_colors_theme.widget_selection_effect.margin_xy(10, 5)
#         widget_colors_theme.widget_font_size = 20
#         widget_colors_theme.set_background_color_opacity(0.5)

#         widget_colors = pygame_menu.Menu(
#             height=self.window_size[1] * 0.7,
#             theme=widget_colors_theme,
#             title='Widget backgrounds',
#             width=self.window_size[0] * 0.8
#         )

#         button_image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_CARBON_FIBER)

#         widget_colors.add.button('Opaque color button', background_color=(100, 100, 100))
#         widget_colors.add.button('Transparent color button', background_color=(50, 50, 50, 200), font_size=40)
#         widget_colors.add.button('Transparent background inflate to selection effect',
#                                  background_color=(50, 50, 50, 200),
#                                  margin=(0, 15)).background_inflate_to_selection_effect()
#         widget_colors.add.button('Background inflate + font background color',
#                                  background_color=(50, 50, 50, 200),
#                                  font_background_color=(200, 200, 200)
#                                  ).background_inflate_to_selection_effect()
#         widget_colors.add.button('This inflates background to match selection effect',
#                                  background_color=button_image,
#                                  font_color=(255, 255, 255), font_size=15
#                                  ).selection_expand_background = True
#         widget_colors.add.button('This is already inflated to match selection effect',
#                                  background_color=button_image,
#                                  font_color=(255, 255, 255), font_size=15
#                                  ).background_inflate_to_selection_effect()

#         self.menu.add.button('Menu with background image', menu_with_bg_image)
#         self.menu.add.button('Test different widget colors', widget_colors)
#         self.menu.add.button('Another fancy button', lambda: print('This button has been pressed'))
#         self.menu.add.button('Quit', pygame_menu.events.EXIT)

#     def main_background(self):
#         background_image = pygame_menu.BaseImage(
#             image_path='Pokemon/graphique/Menu/image/pokemon-wallpaper.jpg',
#             drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL
#         )
#         background_image.draw(self.surface)
#         # Usa il sound_manager già creato invece di crearne un altro
#         self.sound_manager.play()

#     def run_main_loop(self):
#         while True:
#             self.clock.tick(self.fps_limit)

#             # Main menu
#             self.menu.mainloop(self.surface, self.main_background, disable_loop=False, fps_limit=self.fps_limit)

#             # Flip surface
#             pygame.display.flip()

# if __name__ == '__main__':
#     pygame.init()  # Inizializza Pygame
#     main_menu = MainMenu((800, 800), 144)
#     main_menu.run_main_loop()
import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
from typing import Optional


class MainMenu:
    def __init__(self, width: int, height: int):
        self.surface = create_example_window('Example - Image Background', (width, height))
        self.clock = pygame.time.Clock()
        self.main_menu = self.create_main_menu()

    def create_main_menu(self) -> 'pygame_menu.Menu':
        main_menu_theme = pygame_menu.themes.THEME_ORANGE.copy()
        main_menu_theme.set_background_color_opacity(0.5)

        main_menu = pygame_menu.Menu(
            height=self.surface.get_height() * 0.7,
            onclose=pygame_menu.events.EXIT,
            theme=main_menu_theme,
            title='Epic Menu',
            width=self.surface.get_width() * 0.8
        )

        # Aggiungi pulsanti e sottomenu come desiderato
        theme_bg_image = main_menu_theme.copy()
        theme_bg_image.background_color = pygame_menu.BaseImage(
            image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_CARBON_FIBER
        )
        theme_bg_image.title_font_size = 25
        menu_with_bg_image = pygame_menu.Menu(
            height=self.surface.get_height() * 0.7,
            onclose=pygame_menu.events.EXIT,
            theme=theme_bg_image,
            title='Menu with background image',
            width=self.surface.get_width() * 0.8
        )
        menu_with_bg_image.add.button('Back', pygame_menu.events.BACK)

        widget_colors_theme = pygame_menu.themes.THEME_ORANGE.copy()
        widget_colors_theme.widget_margin = (0, 10)
        widget_colors_theme.widget_padding = 0
        widget_colors_theme.widget_selection_effect.margin_xy(10, 5)
        widget_colors_theme.widget_font_size = 20
        widget_colors_theme.set_background_color_opacity(0.5)

        widget_colors = pygame_menu.Menu(
            height=self.surface.get_height() * 0.7,
            theme=widget_colors_theme,
            title='Widget backgrounds',
            width=self.surface.get_width() * 0.8
        )

        button_image = pygame_menu.BaseImage(pygame_menu.baseimage.IMAGE_EXAMPLE_CARBON_FIBER)

        widget_colors.add.button('Opaque color button',
                                background_color=(100, 100, 100))
        widget_colors.add.button('Transparent color button',
                                background_color=(50, 50, 50, 200), font_size=40)
        # Aggiungi altri pulsanti e configurazioni del menu come desiderato
        # ...

        main_menu.add.button('Menu with background image', menu_with_bg_image)
        main_menu.add.button('Test different widget colors', widget_colors)
        main_menu.add.button('Another fancy button', lambda: print('This button has been pressed'))
        main_menu.add.button('Quit', pygame_menu.events.EXIT)

        return main_menu

    def run(self, test: bool = False) -> None:
        while True:
            self.clock.tick(FPS)
            self.main_menu.mainloop(self.surface, self.main_background, disable_loop=test, fps_limit=FPS)
            pygame.display.flip()
            if test:
                break

    def main_background(self) -> None:
        background_image.draw(self.surface)


if __name__ == '__main__':
    # Imposta le costanti e le variabili globali, ad esempio FPS e altre immagini
    FPS = 60
    WINDOW_SIZE = (640, 480)
    background_image = pygame_menu.BaseImage(image_path=pygame_menu.baseimage.IMAGE_EXAMPLE_WALLPAPER)

    # Crea un'istanza della classe MainMenu e avvia il programma
    main_menu_app = MainMenu(*WINDOW_SIZE)
    main_menu_app.run()
