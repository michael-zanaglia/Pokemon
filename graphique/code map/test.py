import pygame
import pygame_menu 
from pygame_menu import sound
import json
import sys
from pygame_menu.widgets import Button
from game import Game  # Assicurati che il modulo "game" sia importato correttamente
pygame.init()



class Menu_game:
    def __init__(self):
        self.width, self.height = 800, 600
        self.surface = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
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

        #charger equipe pokemon
        self.listpoke = "Pokemon/team.json" # Path equipe pokemon
        #charger dialog
        self.dialogo_file_path = 'Pokemon/graphique/code map/dialog.json' # Path dialog.json

        # Img background
        self.background_image = pygame.image.load('Pokemon/graphique/Menu/image/pokemon-wallpaper.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
    def button_action(self, equipe_data):
        print(f"Button clicked for equipe: {equipe_data}")
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

        main_menu_theme.widget_font = pygame_menu.font.FONT_MUNRO

        main_menu = pygame_menu.Menu(
            height=self.height,
            theme=main_menu_theme,
            title='Pokémon',
            width=self.width
        )
        sub_menu_theme = pygame_menu.themes.THEME_BLUE.copy()
        sub_menu_theme.menubar_close_button = False
        sub_menu_theme.background_color = Ctransparent
        sub_menux = pygame_menu.Menu('a', self.width, self.height, theme=sub_menu_theme)
        # Btn personalized
        
        for button in self.equipe_btn():
            
            sub_menux.add.button(*button, self.play_combat, background_color=CtransparentBtn, selection_color=blue, font_size=20, font_color=white)
            # ciao = pygame_menu.widgets.Button(*button, onreturn=None, background_color=CtransparentBtn, selection_color=blue, font_size=20, font_color=white)
            # sub_menux.add.button(ciao)
            

            
        

        sub_menux.add.button('Back', pygame_menu.events.BACK, background_color=CtransparentBtn, selection_color=green, font_size=Fsize, font_color=rouge)

        main_menu.add.button('Play', self.game_run, background_color=Ctransparent, selection_color=blue, font_size=Fsize, font_color=white)
        main_menu.add.button('Play combat', sub_menux, background_color=Ctransparent, selection_color=blue, font_size=Fsize, font_color=white)
        main_menu.add.button('Quit', pygame_menu.events.EXIT, background_color=Ctransparent, selection_color=green, font_size=50, font_color=rouge)
        # Sound
        sound_game = sound.Sound()
        sound_game.set_sound(sound.SOUND_TYPE_CLICK_MOUSE, "Pokemon/graphique/Menu/music/sound/mouse_click.ogg")
        sound_game.set_sound(sound.SOUND_TYPE_EVENT, "Pokemon/graphique/Menu/music/sound/menu_close.ogg")
        sound_game.set_sound(sound.SOUND_TYPE_OPEN_MENU, "Pokemon/graphique/Menu/music/sound/submenu_open.ogg")
        sound
        # Sound set to menu
        main_menu.set_sound(sound_game, recursive=True)
        main_menu.enable()
        return main_menu
    def equipe_btn(self):
        # Nome del file JSON da aprire
        equipe_json_path = "Pokemon/team.json"

        # Apri il file JSON in modalità lettura
        with open(equipe_json_path, 'r') as file_json:
            # Carica il contenuto del file JSON
            dati_json = json.load(file_json)

            # Inizializza una lista di pulsanti
            buttons = []

            # Itera sulla lista
            for equipe in dati_json:
                # Accedi alla chiave (numero) e ai suoi valori (lista di nomi)
                num_equipe = list(equipe.keys())[0]
                nomi_POKEMON = equipe[num_equipe]

                # Aggiungi il pulsante alla lista
                buttons.append((f"EQUIPE: {num_equipe}: {' '.join(nomi_POKEMON)}", self.play_combat))

            return buttons
    def on_resize(self):
        # Check if the window is resized
        window_size = self.surface.get_size()
        self.width, self.height = 1 * window_size[0], 1 * window_size[1]
        main_menu.resize(self.width, self.height)
        print("Resized")


    def run(self, test: bool = False) -> None:
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                    
            # Update the surface
            self.surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            # Call the menu event
            self.on_resize()
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
##########################################################################################

