import pygame
import pygame_menu
import json
from game import Game  # Assicurati che il modulo "game" sia importato correttamente

class Menu_game:
    def __init__(self):
        ####Color####
        self.blu = 255, 0, 0
        self.green = 0, 255, 0
        self.red = 0, 0, 255
        self.width, self.height = 600, 600
        self.surface = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Pokemon - Menu")
        self.main_menu = self.create_main_menu()
        self.clock = pygame.time.Clock()
        # Menu base
        self.menu = pygame_menu.Menu('Welcome', self.width, self.height,
                                     theme=pygame_menu.themes.THEME_BLUE)

        # Music menu ######
        path_music = "Pokemon/graphique/Menu/music/Chill_Travel.mp3"
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound(path_music)
        pygame.mixer.music.load(path_music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        # Img background ######
        self.background_image_path = 'Pokemon/graphique/Menu/image/pokemon-wallpaper.jpg'
        # self.background = pygame_menu.BaseImage(image_path=)
        # pRENDERE LE grandezze con getwidth e get height##################################################

    def create_main_menu(self):  
        mytheme = pygame_menu.themes.THEME_BLUE.copy()
        mytheme.menubar_close_button = False  # Per evitare il pulsante di chiusura sulla barra del menu

        # Imposta il colore di sfondo del menu principale
        mytheme.widget_background_color = (25, 0, 50)

        main_menu = pygame_menu.Menu('Main Menu', self.width, self.height, theme=mytheme)

        main_menu.add.image(image_path='Pokemon/graphique/Menu/image/pokemon-wallpaper.jpg', angle=0, scale=(self.width / 100, self.height / 100))

        main_menu.add.button('Play', self.game_run)
        main_menu.add.button('Play combat', self.play_combat)
        main_menu.add.button('Quit', pygame_menu.events.EXIT)
        return main_menu

    def run(self, test: bool = False) -> None:
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    return

            self.surface.fill((25, 0, 50))
            self.background.draw(self.surface)  # Disegna lo sfondo direttamente
            self.main_menu.update(events)
            self.main_menu.draw(self.surface)
            pygame.display.flip()

            if test:
                break

            pygame.mixer.music.set_volume(0.5)  # Aggiorna il volume della musica
            self.clock.tick(30)  # Regola il frame rate secondo le tue esigenze

    def game_run(self):
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
                break
        main_menu.surface.fill((25, 0, 50))
        main_menu.main_menu.update(events)
        main_menu.main_menu.draw(main_menu.surface)
        pygame.display.flip()
        main_menu.run()
        main_menu.clock.tick()  # Controlla il frame rate
