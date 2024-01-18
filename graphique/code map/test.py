import pygame
import pygame_menu
import time

def on_button_press():
    print("Il bottone è stato premuto!")

def on_submenu_button_press():
    print("Bottone nel sotto-menu premuto!")

# Inizializza pygame
pygame.init()

# Creare un oggetto Menu principale
main_menu = pygame_menu.Menu(300, 400, 'Menu Principale', theme=pygame_menu.themes.THEME_BLUE)

# Aggiungere un bottone al menu principale
main_menu.add.button('Premi Me', on_button_press)

# Creare un oggetto Sotto-Menu
submenu = pygame_menu.Menu(200, 300, 'Sotto-Menu', theme=pygame_menu.themes.THEME_BLUE)

# Aggiungere un bottone al sotto-menu
submenu.add.button('Premi Me Nel Sotto-Menu', on_submenu_button_press)

# Aggiungere il sotto-menu al menu principale
main_menu.add.button('Apri Sotto-Menu', submenu)

# Esegui il loop degli eventi
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Aggiorna il menu principale
    main_menu.mainloop(None, None, disable_loop=True)

    # Puoi eseguire altre azioni qui, ma assicurati che il codice non blocchi l'esecuzione

    # Aggiorna lo schermo (anche se non visibile)
    pygame.display.flip()

    # Introduci un piccolo ritardo per non appesantire la CPU
    time.sleep(0.01)

# Chiudi pygame
pygame.quit()