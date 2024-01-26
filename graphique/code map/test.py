import pygame
import tmx

class CollisionMap:
    def __init__(self, filename):
        self.tiled_map = tmx.TileMap.load(filename)
        self.layers = self.tiled_map.layers

    def check_collision(self, rect):
        for layer in self.layers:
            if isinstance(layer, tmx.ObjectGroup):
                for obj in layer:
                    if obj.type == 'collision' and obj.poly.contains(rect.topleft):
                        return True
        return False

# Esempio di utilizzo
def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    collision_map = CollisionMap('Pokemon/graphique/map0.tmx')  # Sostituisci 'mappa.tmx' con il tuo percorso effettivo

    player_rect = pygame.Rect(100, 100, 32, 32)  # Esempio di rettangolo del giocatore

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Controlla le collisioni del giocatore con la mappa
        if collision_map.check_collision(player_rect):
            # Gestisci la collisione del giocatore con la mappa
            print("Il giocatore ha collisionato con un oggetto nella mappa!")

        screen.fill((255, 255, 255))  # Sostituisci con il tuo disegno dello schermo

        pygame.draw.rect(screen, (0, 0, 255), player_rect)  # Esempio di disegno del giocatore

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
