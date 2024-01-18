import pygame
import pygame_menu
from game import Game
class MainMenu:
    def __init__(self):
        self.width, self.height = 600, 600
        self.surface = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("Pokemon - Menu")
        self.main_menu = self.create_main_menu()
        self.clock = pygame.time.Clock()

        # Img background
        self.background_image_path = 'Pokemon/graphique/Menu/image/pokemon-wallpaper.jpg'
        self.background_image = pygame_menu.BaseImage(image_path=self.background_image_path)

        # Music menu
        path_music = "Pokemon/graphique/Menu/music/Chill_Travel.mp3"
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound(path_music)
        pygame.mixer.music.load(path_music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def create_main_menu(self) -> 'pygame_menu.Menu':
        main_menu_theme = pygame_menu.themes.THEME_BLUE.copy()
        main_menu_theme.set_background_color_opacity(0.5)

        main_menu = pygame_menu.Menu(
            height=self.height * 0.7,
            onclose=pygame_menu.events.EXIT,
            theme=main_menu_theme,
            title='Menu',
            width=self.width * 0.8
        )

        main_menu.add.button('Start New Game', self.start_game)
        main_menu.add.button('Load Game') # Function load
        main_menu.add.button('Settings')# Menu settings
        main_menu.add.button('Quit', pygame_menu.events.EXIT) # exit

        return main_menu

    def run(self, test: bool = False) -> None:
        while True:
            self.clock.tick(30)
            self.main_menu.mainloop(self.surface, self.main_background, disable_loop=test, fps_limit=30)
            pygame.display.flip()
            if test:
                break

    def main_background(self) -> None:
        self.background_image.draw(self.surface)
    
    def start_game(self):
        game = Game()
        game.run()

    def load_game(self):
        # Implementa la logica di caricamento del gioco qui
        print("Caricamento del gioco...")

    def show_settings(self):
        # Implementa la logica per mostrare il menu delle impostazioni qui
        print("Mostra menu impostazioni...")

if __name__ == '__main__':
    pygame.init()
    main_menu_app = MainMenu()

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        main_menu_app.surface.fill((25, 0, 50))
        main_menu_app.main_menu.update(events)
        main_menu_app.main_menu.draw(main_menu_app.surface)

        pygame.display.flip()
