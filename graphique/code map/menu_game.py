import pygame
import pygame_menu

class Menu_gamex:
    def menu_game(self):
        menu_gamex = pygame_menu.Menu(
            height=self.height * 0.7,
            onclose=pygame_menu.events.BACK,
            theme=pygame_menu.themes.THEME_BLUE,
            title='Game Menu',
            width=self.width * 0.8
        )
        menu_gamex.add.button('Map', self.map0())
        menu_gamex.add.button('Pokédex') # Fichier pokedex
        menu_gamex.add.button('Mon equipe') #list mes pokemon
        menu_gamex.add.button('Sauvegarde le jeu') 
        menu_gamex.add.button('Charger le jeu')
        menu_gamex.add.button('Exit')
    def map0(self):
        theme_bg_image = self.menu_game().theme.copy()
        theme_bg_image.background_color = pygame_menu.BaseImage(
        image_path=("Pokemon/graphique/Menu/image/mapsubmenu.png")
        )
        theme_bg_image.title_font_size = 25
        # Crea un nuovo menu con il tema modificato
        menu_with_bg_image = pygame_menu.Menu(
            height=self.height * 0.7,
            onclose=pygame_menu.events.EXIT,
            theme=theme_bg_image,
            title='Menu with background image',
            width=self.width * 0.8
        )
        # Aggiungi altri elementi o pulsanti al nuovo menu, se necessario
        menu_with_bg_image.add.button('Back to Game Menu', pygame_menu.events.BACK)
        menu_with_bg_image.add.button('Another Option')

        # Esegui il nuovo menu
        menu_with_bg_image.mainloop(pygame.display.set_mode((self.width, self.height)))