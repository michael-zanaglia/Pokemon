import pygame
import pygame_menu 
from pygame_menu import sound
import json
import sys
# sys.path.append('C:/Users/Elfo98/Documents/GitHub/Pokemon')
# from poke import Pokemon  # Ora puoi importare normalmente il file poke.py
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
        self.background_image = pygame.image.load('Pokemon/graphique/Menu/image/pokemon-wallpaper.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

         # Music menu
        path_music = "Pokemon/graphique/Menu/music/pokemon_experienceM.mp3"
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound(path_music)
        pygame.mixer.music.load(path_music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def create_main_menu(self):  
        blue = (0, 0, 255, 30)
        green = (0, 255, 0)
        rouge = (255, 0, 0)
        white = (255, 255, 255)
        white_light = (255, 255, 255, 10)
        Ctransparent = (0, 0, 0, 0)
        Ctransparent2 = (0, 0, 0, 50)
        CtransparentBtn = (0, 0, 0, 90)
        CTA_gris = (0, 0, 0, 180)
        Fsize = 30
        
        main_menu_theme = pygame_menu.themes.THEME_BLUE.copy()
        main_menu_theme.menubar_close_button = False
        main_menu_theme.background_color = Ctransparent 
        main_menu_theme.widget_font_color = rouge  # Colore del testo dei widget
        main_menu_theme.widget_background_color = Ctransparent2  # Colore di sfondo del pulsante
        main_menu_theme.widget_border_color = rouge  # Colore del bordo del widget
        main_menu_theme.widget_font = pygame_menu.font.FONT_MUNRO

        main_menu = pygame_menu.Menu(
            height=self.height,
            theme=main_menu_theme,
            title='Pokémon',
            width=self.width
        )
    ### Sub MENU ###
        sub_menu_theme = pygame_menu.themes.THEME_BLUE.copy()
        sub_menu_theme.title_font_color = white  # Colore del testo del titolo del menu
        sub_menu_theme.widget_font_color = white_light  # Colore del testo dei widget
        sub_menu_theme.widget_selection_color = blue  # Colore del pulsante selezionato
        sub_menu_theme.widget_background_color = CtransparentBtn  # Colore di sfondo del pulsante
        sub_menu_theme.widget_border_color = CTA_gris  # Colore del bordo del widget
        sub_menu_theme.selection_color = blue  # Colore dell'indicatore di selezione
        sub_menu_theme.title_background_color = CtransparentBtn  # Colore di sfondo del titolo del menu
        sub_menu_theme.menubar_close_button = False # Disabilita il pulsante di chiusura della barra dei menu
        sub_menu_theme.background_color = Ctransparent   # Colore di sfondo del menu
        sub_menu_theme.widget_font = pygame_menu.font.FONT_MUNRO
    ### MENU ### Choix adversaire ###
        num = 0 
        choix_adversaire = pygame_menu.Menu(' Choix Adversaire ', self.width, self.height, theme=sub_menu_theme)
        for button in self.equipe_btn():
            choix_adversaire.add.button(*button, self.choix_adversaire, font_size=20)
            num += 1 
            print(f"{num}")
        choix_adversaire.add.button('Back', pygame_menu.events.BACK, background_color=CtransparentBtn, selection_color=green, font_size=Fsize, font_color=rouge)
    ### MENU ### Choix equipe ###
        choix_equipe = pygame_menu.Menu(' Choix Equipe ', self.width, self.height, theme=sub_menu_theme)
        num = 0
        for button in self.adversaire_btn():
            choix_equipe.add.button(*button, self.choix_equipe, background_color=CTA_gris, selection_color=blue, font_size=20, font_color=white)
            num += 1
            print(f"{num}")
        choix_equipe.add.button('Back', pygame_menu.events.BACK, background_color=CtransparentBtn, selection_color=green, font_size=Fsize, font_color=rouge)
    ### MENU ### Sub menu play combat###
        sub_menu_play = pygame_menu.Menu("Play combact", self.width, self.height, theme=sub_menu_theme)
        sub_menu_play.add.button(choix_adversaire.get_title(), choix_adversaire)
        sub_menu_play.add.button(choix_equipe.get_title(), choix_equipe)
    ### MAIN ### MENU ###
        main_menu.add.button('Play', self.game_run, background_color=CtransparentBtn, selection_color=blue, font_size=Fsize, font_color=white)
        main_menu.add.button('Play combat', sub_menu_play, background_color=CtransparentBtn, selection_color=rouge, font_size=Fsize, font_color=white)
        main_menu.add.button('Quit', pygame_menu.events.EXIT, background_color=Ctransparent, selection_color=green, font_size=50, font_color=rouge)
        
        sound_game = sound.Sound()
        sound_game.set_sound(sound.SOUND_TYPE_CLICK_MOUSE, "Pokemon/graphique/Menu/music/sound/mouse_click.ogg")
        sound_game.set_sound(sound.SOUND_TYPE_CLOSE_MENU, "Pokemon/graphique/Menu/music/sound/menu_close.ogg")
        sound_game.set_sound(sound.SOUND_TYPE_WIDGET_SELECTION, "Pokemon/graphique/Menu/music/sound/menu_back.ogg")
        sound_game.set_sound(sound.SOUND_TYPE_OPEN_MENU, "Pokemon/graphique/Menu/music/sound/submenu_open.ogg")
        
        main_menu.set_sound(sound_game, recursive=True)
        main_menu.enable()
        return main_menu
    def adversaire_btn(self):
        adversaire_json_path = "Pokemon/trainer.json"
        with open(adversaire_json_path, 'r') as file_json:
            dati_json = json.load(file_json)
            button = []
            for adversaire in dati_json:
                num_equipe = list(adversaire.keys())[0]
                nomi_POKEMON = adversaire[num_equipe]
                button.append((f"{num_equipe}: {' '.join(nomi_POKEMON)}", self.choix_adversaire))
            return button
        
    def equipe_btn(self):
        equipe_json_path = "Pokemon/team.json"
        
        with open(equipe_json_path, 'r') as file_json:
            dati_json = json.load(file_json)
            buttons = []
            for equipe in dati_json:
                num_equipe = list(equipe.keys())[0]
                nomi_POKEMON = equipe[num_equipe]
                buttons.append((f"EQUIPE: {num_equipe}: {' '.join(nomi_POKEMON)}", self.choix_equipe))
            return buttons

    def on_resize(self):
        window_size = self.surface.get_size()
        self.width, self.height = window_size[0], window_size[1]
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        self.main_menu = self.create_main_menu()


    def run(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    self.surface = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.on_resize()
            self.surface.blit(self.background_image, (0, 0))  
            self.main_menu.update(events)
            self.main_menu.draw(self.surface)
            pygame.display.flip()
            self.clock.tick(30)

    def game_run(self):
        pygame.mixer.music.stop()
        path_music_jeu = "Pokemon/graphique/Menu/music/Focus Minimal Minimal 120.mp3"
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound(path_music_jeu)
        pygame.mixer.music.load(path_music_jeu)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        game = Game()
        game.run()
# A FAIRE
    def choix_adversaire(self, button_text):
        choice = button_text.split(":")[1].strip()
        print("Scelta dell'avversario: ", choice)
#       Pokemon.choix_Adversaire(choice)
        #ajouter une méthode qui fait que le joueur 2 prend l'équipe
        pass
    def choix_equipe(self, button_text):
        # Richiama la funzione start_combat di poke.py passando la scelta della squadra
        choice = button_text.split(':')[1].strip()  # Estrai la scelta dopo il primo ":" e rimuovi eventuali spazi
        print("Scelta della squadra: ", choice)
 #       Pokemon.choix_Equipe(choice)
        #ajouter une méthode qui fait que le joueur 1 prend l'équipe
        pass

if __name__ == '__main__':
    main_menu = Menu_game()
    main_menu.run()