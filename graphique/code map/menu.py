import pygame
import pygame_menu 
from pygame_menu import sound
import json
import sys
# sys.path.append('C:/Users/Elfo98/Documents/GitHub/Pokemon')
# from poke import Pokemon  # Now you can import the poke.py file normally
from pygame_menu.widgets import Button
from game import Game  # Make sure the "game" module is correctly imported

pygame.init()

class Menu_game:
    def __init__(self):
        # Window dimensions
        self.width, self.height = 800, 600
        self.surface = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("Pokemon - Menu")
        # Create the main menu
        self.main_menu = self.create_main_menu()
        self.clock = pygame.time.Clock()
        # Load background image
        self.background_image = pygame.image.load('Pokemon/graphique/Menu/image/pokemon-wallpaper.jpg')
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))

         # Music for the menu
        path_music = "Pokemon/graphique/Menu/music/pokemon_experienceM.mp3"
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound(path_music)
        pygame.mixer.music.load(path_music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def create_main_menu(self): 
        # Colors 
        blue = (0, 0, 255)
        green = (0, 255, 0)
        red = (255, 0, 0)
        white = (255, 255, 255)
        # Transparent backgrounds
        transparent = (0, 0, 0, 50)
        transparent2 = (0, 0, 0, 0)
        transparent_button = (0, 0, 0, 90)
        # Font size
        font_size = 60
        # Pokemon font
        font = pygame.font.Font('Pokemon/graphique\Menu\Font\pokemon_pixel_font.ttf', font_size)
        # MENU THEMES #
        main_menu_theme = pygame_menu.themes.THEME_BLUE.copy()
        main_menu_theme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_NONE
        main_menu_theme.menubar_close_button = False
        main_menu_theme.background_color = transparent2  
        main_menu_theme.title_font = font
        main_menu_theme.widget_font = pygame_menu.font.FONT_MUNRO
        main_menu_theme.widget_margin = (0,10) # (x,y) in pixels
        
        # Create the main MENU
        main_menu = pygame_menu.Menu(
            height=self.height,
            theme=main_menu_theme,
            title='',
            width=self.width
        )
        
    ### MENU ### Opponent Selection ###
        num = 0 
        opponent_selection = pygame_menu.Menu(' Opponent Selection ', self.width, self.height, theme=main_menu_theme)
        
        for button in self.team_btn():
            opponent_selection.add.button(*button, self.opponent_choice, background_color=transparent_button, selection_color=red, font_size=20, font_color=white)
            num += 1 
            print(f"{num}")
    ### MENU ### Team Selection ###
        team_selection = pygame_menu.Menu(' Team Selection ', self.width, self.height, theme=main_menu_theme)
        
        num = 0
        for button in self.opponent_btn():
            team_selection.add.button(*button, self.team_choice, background_color=transparent_button, selection_color=blue, font_size=20, font_color=white)
            num += 1
            print(f"{num}")
        team_selection.add.button('Back', pygame_menu.events.BACK, background_color=transparent_button, selection_color=green, font_size=font_size, font_color=red)
        team_selection.menubar_close_button = False
    ### MENU ### Submenu Selection###
        sub_menu_play = pygame_menu.Menu("", self.width, self.height, theme=main_menu_theme)
        sub_menu_play.add.button(opponent_selection.get_title(), opponent_selection, background_color=transparent, selection_color=blue, font_size=font_size, font_color=white)
        sub_menu_play.add.button(team_selection.get_title(), team_selection, background_color=transparent, selection_color=blue, font_size=font_size, font_color=white)
        sub_menu_play.menubar_close_button = False
    ### MAIN ### MENU ###
        main_menu.add.button('Play', self.game_run, background_color=transparent, selection_color=blue, font_size=font_size, font_color=white) # Button run game 2d
        main_menu.add.button('Play combat', sub_menu_play, background_color=transparent, selection_color=blue, font_size=font_size, font_color=white) # Button to sub menu
        main_menu.add.button('Quit', pygame_menu.events.EXIT, background_color=transparent, selection_color=green, font_size=50, font_color=red)
        # Menu Sound #
        sound_game = sound.Sound()
        sound_game.set_sound(sound.SOUND_TYPE_CLICK_MOUSE, "Pokemon/graphique/Menu/music/sound/mouse_click.ogg")
        sound_game.set_sound(sound.SOUND_TYPE_CLOSE_MENU, "Pokemon/graphique/Menu/music/sound/menu_close.ogg")
        sound_game.set_sound(sound.SOUND_TYPE_WIDGET_SELECTION, "Pokemon/graphique/Menu/music/sound/menu_back.ogg")
        sound_game.set_sound(sound.SOUND_TYPE_OPEN_MENU, "Pokemon/graphique/Menu/music/sound/submenu_open.ogg")
        
        main_menu.set_sound(sound_game, recursive=True)
        main_menu.enable()
        return main_menu
    # Method to get opponents
    def opponent_btn(self):
        opponent_json_path = "Pokemon/trainer.json"
        with open(opponent_json_path, 'r') as file_json:
            json_data = json.load(file_json)
            button = []
            for opponent in json_data:
                team_number = list(opponent.keys())[0]
                pokemon_names = opponent[team_number]
                button.append((f"{team_number}: {' '.join(pokemon_names)}", self.opponent_choice))
            return button
    # Method to get teams
    def team_btn(self):
        team_json_path = "Pokemon/team.json"
        
        with open(team_json_path, 'r') as file_json:
            json_data = json.load(file_json)
            buttons = []
            for team in json_data:
                team_number = list(team.keys())[0]
                pokemon_names = team[team_number]
                buttons.append((f"TEAM: {team_number}: {' '.join(pokemon_names)}", self.team_choice))
            return buttons
    # Resize Windows
    def on_resize(self):
        window_size = self.surface.get_size()
        self.width, self.height = window_size[0], window_size[1]
        self.background_image = pygame.transform.scale(self.background_image, (self.width, self.height))
        self.main_menu = self.create_main_menu()

    # Main Run
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
        path_game_music = "Pokemon/graphique/Menu/music/Focus Minimal Minimal 120.mp3"
        pygame.mixer.init()
        self.click_sound = pygame.mixer.Sound(path_game_music)
        pygame.mixer.music.load(path_game_music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
        game = Game()
        game.run()
# TO DO
    def opponent_choice(self, button_text):
        choice = button_text.split(":")[1].strip()
        print("Opponent choice: ", choice)
#       Pokemon.opponent_choice(choice)
        # Add a method for player 2 to take the team
        pass
    def team_choice(self, button_text):
        # Call the start_combat function from poke.py passing the team choice
        choice = button_text.split(':')[1].strip()  # Extract choice after first ":" and remove any spaces
        print("Team choice: ", choice)
 #       Pokemon.team_choice(choice)
        # Add a method for player 1 to take the team
        pass

if __name__ == '__main__':
    main_menu = Menu_game()
    main_menu.run()