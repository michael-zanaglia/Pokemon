import pygame
import pygame_menu
import json
from game import Game
class MainMenu:
    def __init__(self):
        self.width, self.height = 600, 600
        self.surface = pygame.display.set_mode((self.width, self.height))
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

        self.listadversaire = self.load_trainers()  # Inizializza listadversaire con la lista degli allenatori


        self.listpoke = "Pokemon/team.json"
        self.dialogo_file_path = 'Pokemon/graphique/code map/dialog.json'
        self.dialogo = self.load_dialogo(self.dialogo_file_path)


    def load_dialogo(self, percorso_file_json):
        with open(percorso_file_json, 'r') as file:
            return json.load(file)
        
    def load_trainers(self):
        file_enemi = "Pokemon/trainer.json"
        with open(file_enemi, 'r') as file:
            trainers_data = json.load(file)

        # Estrai il nome degli allenatori dalla struttura dati
        trainers_list = []
        for trainer_data in trainers_data:
            for key, names_list in trainer_data.items():
                trainers_list.extend(names_list)

        return trainers_list
    def create_menus(self):
        # Menu principale
        self.main_menu = self.create_main_menu()

        # Sottomenu
        self.sub_0 = self.create_sub_menu0()

        # Imposta la gestione dell'evento onclose direttamente durante la creazione del sottomenu
        self.sub_0.add_button('Return to Main Menu', self.return_to_main_menu, font_size=20)

        # Aggiunge il sottomenu come sottomenu del menu principale
        self.main_menu.add_submenu(self.sub_0)

    def create_main_menu(self) -> 'pygame_menu.Menu':
        main_menu_theme = pygame_menu.themes.THEME_BLUE
        main_menu_theme.set_background_color_opacity(0.3)
        main_menu = pygame_menu.Menu(
            height=self.height * 0.7,
            onclose=pygame_menu.events.EXIT,
            theme=main_menu_theme,
            title='Menu',
            width=self.width * 0.8
        )

        main_menu.add.button('Start New Game', self.start_game)
        main_menu.add.button('Load combact', self.create_sub_menu0) # Function load
        main_menu.add.button('Settings')# Menu settings
        main_menu.add.button('Quit', pygame_menu.events.EXIT) # exit

        return main_menu
    
    def create_sub_menu0(self):
        sub_0_theme = pygame_menu.themes.THEME_DARK
        sub_0_theme.set_background_color_opacity(0.2)

        sub_0 = pygame_menu.Menu(
            height=self.height * 0.7,
            onclose=pygame_menu.events.BACK,
            theme=sub_0_theme,
            title="Prima di iniziare",
            width=self.width * 0.8
        )
        sub_0.add.button('Start New Game', self.start_game)
        sub_0.add.button('Load combact', self.sub_menu0) # Function load
        sub_0.add.button('Settings')# Menu settings
        sub_0.add.button('Quit', pygame_menu.events.EXIT) # exit

    def run(self, test: bool = False) -> None:
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return  # Termina il ciclo quando l'utente chiude la finestra
            self.main_menu.mainloop(self.surface, self.main_background, disable_loop=test, fps_limit=30)
            pygame.display.flip()
            if test:
                break

    

    def get_enemi(self, avversario):
        print(f"Avversario selezionato: {avversario}")

    def get_equipe(self):
        with open(self.listpoke, 'r') as file:
            data = json.load(file)

        equipe = data  # Ora `equipe` è direttamente la lista
        self.equipe_pokemon = [(str(i + 1), pokemon) for i, pokemon in enumerate(equipe)]
        return self.equipe_pokemon
    
    def main_background(self) -> None:
        self.background_image.draw(self.surface)
    
    def start_game(self):
        game = Game()
        game.run()

    def load_teams(self):
        with open(self.listpoke, 'r') as file:
            data = json.load(file)
        return data

    def stampa_lista_testo(self, chiave_dialogo):
        # Mostra la lista di testo associata alla chiave del dialogo
        dialogo = self.dialogo.get(chiave_dialogo, [])
        for frase in dialogo:
            personaggio = frase.get('personaggio', '')
            testo = frase.get('testo', '')
            print(f"{personaggio}: {testo}")

if __name__ == '__main__':
    pygame.init()
    main_menu_app = MainMenu()

    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                break
        main_menu_app.run(False)
        main_menu_app.surface.fill((25, 0, 50))
        main_menu_app.main_menu.update(events)
        main_menu_app.main_menu.draw(main_menu_app.surface)

        pygame.display.flip()
