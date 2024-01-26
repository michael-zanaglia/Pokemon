import pygame
import pygame_menu
import sys
from game import Game  # Assicurati che il modulo "game" sia importato correttamente

class Menu_game:
    def __init__(self):
        self.width, self.height = 800, 600
        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pokemon - Menu")
        self.main_menu = self.create_main_menu()
        self.clock = pygame.time.Clock()

        # Music menu
        path_music = "Pokemon/graphique/Menu/music/pokemon_experienceM.mp3"
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound(path_music)
        pygame.mixer.music.load(path_music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)


        # Img background
        self.background_image = pygame.image.load('Pokemon/graphique/Menu/image/pokemon-wallpaper.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

    def create_main_menu(self):  
        # Variable color
        blue = (0, 0, 255)
        green = (0, 255, 0)
        rouge = (255, 0, 0)
        white = (255, 255, 255)
        Ctransparent = (0, 0, 0, 50)
        Ctransparent2 = (0, 0, 0, 0)
        CtransparentBtn = (0, 0, 0, 90)
        Fsize = 30
        # Creation du menu
        main_menu_theme = pygame_menu.themes.THEME_BLUE.copy()
        main_menu_theme.menubar_close_button = False
        main_menu_theme.background_color = Ctransparent2  # Imposta il colore di sfondo del menu principale
        # main_menu_theme.set_background_color_opacity(0.5)  # 50% opacity

        main_menu = pygame_menu.Menu(
            height=self.height,
            theme=main_menu_theme,
            title='Pokémon',
            width=self.width
        )
        sub_menu_theme = pygame_menu.themes.THEME_BLUE.copy()
        sub_menu_theme.menubar_close_button = False
        sub_menu_theme.background_color = Ctransparent
        sub_menux = pygame_menu.Menu('Sub Menu', self.width, self.height, theme=sub_menu_theme)
        sub_menux.add.button('Button 1', self.play_combat, background_color=CtransparentBtn, selection_color=blue, font_size=Fsize, font_color=white)
        sub_menux.add.button('Button 2', self.play_combat, background_color=CtransparentBtn, selection_color=blue, margin=(0, 15), font_size=Fsize, font_color=white).background_inflate_to_selection_effect()
        sub_menux.add.button('Back', pygame_menu.events.BACK, background_color=CtransparentBtn, selection_color=green, font_size=Fsize, font_color=rouge)

        main_menu.add.button('Play', self.game_run, background_color=Ctransparent, selection_color=blue, font_size=Fsize, font_color=white)
        main_menu.add.button('Play combat', sub_menux, background_color=Ctransparent, selection_color=blue, font_size=Fsize, font_color=white)
        main_menu.add.button('Quit', pygame_menu.events.EXIT, background_color=Ctransparent, selection_color=green, font_size=50, font_color=rouge)

        return main_menu
    def run(self, test: bool = False) -> None:
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()

            self.surface.blit(self.background_image, (0, 0))  # Disegna lo sfondo
            self.main_menu.update(events)
            self.main_menu.draw(self.surface)
            pygame.display.flip()

            if test:
                break

            pygame.mixer.music.set_volume(0.5)
            self.clock.tick(30)
    def game_run(self):
        pygame.mixer.music.stop()
        # Music JEU
        path_music_jeu = "Pokemon/graphique/Menu/music/Focus Minimal Minimal 120.mp3"
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound(path_music_jeu)
        pygame.mixer.music.load(path_music_jeu)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        game = Game()
        game.run()

    def play_combat(self):
        # Implementa la logica per avviare il combattimento
        pass

if __name__ == '__main__':
    pygame.init()
    main_menu = Menu_game()

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

        main_menu.main_menu.update(events)
        main_menu.main_menu.draw(main_menu.surface)
        pygame.display.flip()
        main_menu.run()
        main_menu.clock.tick(30)
